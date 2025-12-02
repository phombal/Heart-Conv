# Baseline vs. Full Agent Comparison

## Purpose
This document explains the differences between `base-assistant.py` (baseline) and `assistant.py` (full system) to help understand what each component contributes to performance.

---

## Architecture Comparison

### Base Assistant (`base-assistant.py`)
```
┌─────────────────────────────┐
│   Single Agent              │
│   - Basic instructions      │
│   - No tools                │
│   - No handoffs             │
│   - Common sense reasoning  │
└─────────────────────────────┘
```

**Components:**
- 1 agent (Base Assistant)
- 0 tools
- ~20 lines of simplified instructions

### Full Assistant (`assistant.py`)
```
┌─────────────────────────────────────────────────┐
│              Assistant Agent                     │
│   - Detailed protocol instructions               │
│   - Tool: call_recommendation_agent             │
│   - Tool: call_verification_agent               │
└──────────────┬──────────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
┌──────────────┐  ┌──────────────┐
│ Recommendation│  │ Verification │
│    Agent      │  │    Agent     │
│               │  │              │
│ Tools:        │  └──────────────┘
│ - checkNot    │
│   Emergency   │
│ - check_arb   │
│ - check_arni  │
│ - check_aldo  │
│ - check_beta  │
│ - check_sgc   │
│ - check_sglt2 │
│ - check_hydra │
└───────────────┘
```

**Components:**
- 3 main agents (Assistant, Recommendation, Verification)
- 8+ medication checker agents
- 1 emergency checker tool
- ~380 lines of detailed protocol instructions

---

## Feature Comparison

| Feature | Base Assistant | Full Assistant |
|---------|---------------|----------------|
| **Agent Handoffs** | ❌ None | ✅ Recommendation → Verification |
| **Tool Calling** | ❌ None | ✅ 8+ medication checkers |
| **Emergency Detection** | ❌ Manual logic | ✅ Automated `checkNotEmergency` |
| **Contraindication Checking** | ❌ None | ✅ Per-medication agents |
| **Titration Protocol** | ❌ Basic reasoning | ✅ Detailed dosing guidelines |
| **Verification Step** | ❌ None | ✅ Separate verification agent |
| **Hold/Discontinue Criteria** | ❌ General guidance | ✅ Specific thresholds per drug |
| **Lab Monitoring** | ❌ None | ✅ Protocol-specified requirements |

---

## Instruction Complexity

### Base Assistant Instructions
- **Length:** ~25 lines
- **Content:**
  - Basic symptom collection
  - Simple vital sign gathering
  - General "call your doctor" guidance
  - No specific dosing information
  - No contraindication knowledge

### Full Assistant Instructions
- **Length:** ~50 lines (Assistant) + ~380 lines (Recommendation) + ~200 lines (Verification)
- **Content:**
  - Detailed symptom assessment
  - Structured summary generation
  - Mandatory tool calling workflow
  - Specific titration strategies
  - 8 medication classes with:
    - Starting doses
    - Incremental titration steps
    - Maximum doses
    - Contraindications
    - Hold/discontinue criteria
    - Lab monitoring requirements

---

## Expected Performance Differences

### Base Assistant (Expected Weaknesses)
1. **Safety:** May miss contraindications or dangerous vital sign combinations
2. **Correctness:** Lacks specific dosing guidelines, may recommend incorrect doses
3. **Optimal:** No structured titration strategy, may be inefficient
4. **Empathetic:** Should be similar (conversational style in both)

### Full Assistant (Expected Strengths)
1. **Safety:** Automated checks for contraindications and emergency conditions
2. **Correctness:** Protocol-compliant recommendations with verification
3. **Optimal:** Structured titration strategies (single-drug vs. multi-drug)
4. **Empathetic:** Should be similar (conversational style in both)

---

## Running Comparisons

### Run Base Assistant
```bash
./venv/bin/python simulation.py -n 20 -b 5 -a base-assistant.py -o base-assistant-results
```

### Run Full Assistant
```bash
./venv/bin/python simulation.py -n 20 -b 5 -a assistant.py -o assistant-results
```

### Compare Results
Look at:
- **Per-Round Scores:** SAFE, CORRECT, OPTIMAL, EMPATHETIC
- **Protocol Outcomes:** Endpoint distribution (success vs. failure)
- **Safety Metrics:** Auto-failures, critical safety issues
- **Conversation Quality:** Naturalness, completeness

---

## Hypothesis

The full assistant should significantly outperform the baseline on:
1. **SAFE score** (due to automated contraindication checking)
2. **CORRECT score** (due to detailed protocol knowledge)
3. **OPTIMAL score** (due to structured titration strategies)

The baseline may be comparable on:
1. **EMPATHETIC score** (both use conversational style)
2. **Basic symptom collection** (both follow similar structure)

---

## Key Takeaway

The baseline serves as a **minimum viable product** - it can have a conversation and collect information, but lacks the sophisticated medical knowledge and safety checks needed for actual clinical deployment. The performance gap between baseline and full system quantifies the value of:
- Multi-agent orchestration
- Detailed protocol encoding
- Automated safety verification

