# Evaluation System Architecture

## Overview
The evaluation system in `simulation.py` is a multi-layered, LLM-judge-based framework that assesses heart failure medication titration agents across multiple dimensions, using both autoed rule-based checks and sophisticated natural language evaluation.

---

## 1. **Multi-Dimensional Rubric with Weighted Scoring**

The core evaluation uses a **4-axis rubric** implemented via the `EncounterEvaluation` Pydantic model:

- **SAFE (0-5)**: Safety & contraindication checks
  - Weight: **35%** (highest priority)
  - Assesses vital sign monitoring, lab ordering, contraindication avoidance, hold/discontinue criteria
  - Encodes detailed medication-specific safety thresholds (e.g., "Hold ACE-I if K+ >5.5 mEq/L")

- **CORRECT (0-5)**: Guideline-consistent clinical correctness
  - Weight: **30%**
  - Evaluates dosing accuracy, titration sequence, medication appropriateness
  - Validates against protocol-specified incremental doses and maximum doses

- **OPTIMAL (0-5)**: Efficiency & long-term planning
  - Weight: **20%**
  - Checks for explicit next dose, timing, lab monitoring schedule, follow-up plan, contingency planning
  - Assesses patient-specific considerations (renal function, adherence barriers, comorbidities)

- **EMPATHETIC (0-5)**: Communication & patient-centeredness
  - Weight: **15%**
  - Evaluates language appropriateness, teach-back usage, adherence support strategies
  - Considers medical literacy matching and emotional validation

**Weighted Score Calculation:**
```python
weighted_score = (0.35 * safe + 0.30 * correct + 0.20 * optimal + 0.15 * empathetic) / 5.0
# Normalized to [0, 1] scale
```

---

## 2. **Hybrid Evaluation: Automated Checks + LLM Judge**

The system combines **rule-based automation** with **LLM-based judgment** for comprehensive coverage:

### Automated Checks (Pre-LLM)
Implemented as Python functions that scan agent responses for protocol violations:

- **`check_vitals_in_titration_range()`**: Flags titration attempts when BP <80/40 or >200/110, or HR <50
- **`check_arni_washout_period()`**: Detects ARNI initiation without 48-hour ACE-I washout
- **`check_max_dose_violations()`**: Catches recommendations exceeding protocol maximum doses
- **`check_forbidden_actions()`**: Matches against scenario-specific forbidden actions (e.g., "increase_beta_blocker_when_hr_<50")
- **`check_required_actions()`**: Ensures critical actions from scenario `hidden_eval` are performed
- **`check_escalation_thresholds()`**: Validates appropriate escalation when vitals breach critical thresholds

These checks produce an `auto_failures` list that is:
1. Passed to the LLM judge as context
2. Included in the final `EncounterEvaluation` output
3. Used for early termination decisions

### LLM Judge Evaluation
An OpenAI agent (`judge_agent`) with ~200 lines of detailed medical protocol instructions:

- Receives: patient context, vitals, medications, agent response, automated failures
- Produces: Structured `EncounterEvaluation` with scores, reasoning, and notes
- Uses **Pydantic output schema** for reliable JSON extraction
- Incorporates automated failures into scoring (e.g., auto-failure → lower SAFE score)

---

## 3. **Per-Round Evaluation (Not Per-Turn)**

To reduce JSON file size and provide holistic assessment, evaluation occurs **once per round** (not per conversation turn):

```python
async def evaluate_full_round(
    round_history: List[Dict[str, Any]],  # All turns in the round
    scenario: Dict[str, Any],
    encounter_data: Dict[str, Any],
    auto_failures: List[str]  # Accumulated from all turns
) -> EncounterEvaluation
```

**Process:**
1. Agent and patient exchange multiple turns (up to 10 per round)
2. Auto-failures are collected during each turn but not evaluated immediately
3. After round completes, **one comprehensive evaluation** assesses all 4 dimensions across the entire round
4. Result: Single `EncounterEvaluation` per round (vs. 10+ evaluations per round in old system)

**Benefits:**
- 60% reduction in JSON file size
- More coherent assessment of overall round quality
- Captures multi-turn patterns (e.g., agent gathering info across 3 turns before making recommendation)

---

## 4. **Three-Level Outcome Classification**

Beyond per-round scores, the system evaluates outcomes at multiple granularities:

### Level 1: Protocol Outcome (`ProtocolOutcome` model)
Classifies the **entire conversation** into one of 8 endpoints:

1. **complete_success**: All target doses reached, patient graduates
2. **partial_success**: Some drugs reach targets, others plateau at submaximal doses
3. **non_adherence_failure**: Progressive missed doses, program discontinuation
4. **side_effect_failure**: Problematic adverse effects, early termination
5. **acute_decompensation_ed_referral**: Acute worsening, ED referral
6. **hospitalization_pause**: Hospital admission, program suspension
7. **patient_withdrawal**: Patient refuses to continue
8. **incomplete**: Conversation ended prematurely

**Evaluated by:** `protocol_outcome_agent` (separate LLM agent with endpoint-specific instructions)

**Tracks:**
- Medication progression (starting dose → final dose vs. target dose)
- Safety events (vital violations, lab abnormalities)
- Adherence issues
- Overall protocol success (boolean)

### Level 2: Assignment Compliance (`AssignmentComplianceEvaluation` model)
Assesses whether agent follows the **CS224V assignment instructions** across 7 dimensions:

1. Information gathering (symptoms, side effects, adherence)
2. Question answering
3. Protocol-based recommendation
4. Physician approval process
5. Patient communication
6. Titration strategy followed (single-drug vs. multi-drug)
7. Protocol adherence (dosing, safety, monitoring)

**Evaluated by:** `assignment_compliance_agent` (separate LLM agent)

**Output:** Compliance score (0-1) = average of 7 dimension scores / 5.0

### Level 3: Simplified Metrics (`SimplifiedMetrics` model)
Lightweight summary statistics:

- Strategy (single_drug, multi_drug, unknown)
- Difficulty (easy, moderate, adversarial, unknown)
- Total turns and rounds
- Total auto-failures
- Critical safety issues (rounds with SAFE ≤ 1)

---

## 5. **Asynchronous Batch Processing with Immediate Persistence**

The simulation engine uses **asyncio** for concurrent execution:

```python
# Run N conversations concurrently in batches of B
for i in range(0, total_scenarios, batch_size):
    batch = scenarios[i:i+batch_size]
    batch_tasks = [
        run_single_conversation(scenario, idx, total, output_dir, AgentClass)
        for idx, scenario in enumerate(batch, start=i)
    ]
    batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
```

**Key Features:**
- **Batch size configurable** via `-b/--batch-size` (default: 5)
- **Immediate file saving**: Each conversation writes its JSON file as soon as it completes (not waiting for batch)
- **Graceful error handling**: Exceptions captured per-conversation, don't crash entire batch
- **Progress tracking**: Real-time console output with conversation IDs, scores, and outcomes

**Performance:**
- 20 scenarios with batch_size=5 → ~4 batches → ~4x speedup vs. sequential
- Rate limiting: 0.3s sleep between turns to avoid API throttling

---

## 6. **Dynamic Agent Loading and Multi-Round Support**

### Dynamic Agent Loading
The system can evaluate **different agent implementations** without code changes:

```python
AssistantOrchestratorClass = load_agent_module(args.agent)
# Loads from assistant.py, base-assistant.py, or any custom file
```

**Usage:**
```bash
python simulation.py -a assistant.py     # Full multi-agent system
python simulation.py -a base-assistant.py # Baseline single agent
```

### Multi-Round Scenarios
Supports simulating **longitudinal titration journeys** (multiple check-ins over weeks):

```json
{
  "id": "HF_CONV_001",
  "rounds": [
    {"round": 1, "week": 0, "conversation_goal": "Initial assessment..."},
    {"round": 2, "week": 4, "conversation_goal": "Follow-up after Losartan increase..."},
    {"round": 3, "week": 8, "conversation_goal": "Declining adherence..."}
  ]
}
```

**Implementation:**
- Each round gets its own patient simulator agent with round-specific context
- Conversation history persists across rounds (agent "remembers" previous rounds)
- Each round evaluated independently, but protocol outcome considers full journey
- Enables testing of long-term strategy adherence and multi-week symptom tracking

---

## Summary

The evaluation architecture is a **sophisticated, production-grade system** that:

1. ✅ Uses a **weighted 4-axis rubric** (SAFE/CORRECT/OPTIMAL/EMPATHETIC) with medical protocol encoding
2. ✅ Combines **automated rule-based checks** with **LLM judge evaluation** for comprehensive coverage
3. ✅ Performs **per-round evaluation** (not per-turn) to reduce overhead and improve coherence
4. ✅ Classifies outcomes at **3 levels** (protocol endpoint, assignment compliance, simplified metrics)
5. ✅ Supports **asynchronous batch processing** with immediate file persistence for efficiency
6. ✅ Enables **dynamic agent loading** and **multi-round scenarios** for flexible experimentation

This design balances **clinical rigor** (detailed safety checks, protocol adherence), **scalability** (batch processing, per-round evaluation), and **flexibility** (pluggable agents, multi-round support) to provide a robust framework for evaluating conversational medical AI agents.

