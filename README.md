# Heart Failure Medication Titration Agent

An AI-powered healthcare assistant for guiding heart failure patients through medication titration protocols. The system uses LLM-based agents to provide safe, evidence-based medication adjustments while monitoring patient vitals and ensuring protocol adherence.

## 📋 Overview

This project implements an intelligent agent system that:
- Conducts patient conversations about heart failure medications
- Monitors vital signs and lab values for safety
- Recommends medication titration based on clinical guidelines
- Escalates to physician approval when needed
- Verifies clinical appropriateness of recommendations
- Evaluates conversation quality across 4 dimensions (SAFE, CORRECT, OPTIMAL, EMPATHETIC)

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- OpenAI API key

### Environment Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd cs224v-final-project-1
```

2. **Create and activate virtual environment**
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

Required packages:
- `openai>=2.0.0` - OpenAI API client
- `pydantic>=2.7.0` - Data validation
- `openai-agents` - OpenAI Agents SDK

4. **Set up OpenAI API key**

Choose one of the following methods:

**Option A: Environment variable**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

**Option B: `.env` file** (recommended)
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

**Option C: Add to shell profile** (persistent)
```bash
# For bash
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc

# For zsh
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

## 📊 Running the Prototype

### 1. Run Single Patient Conversation (Interactive)

Run the assistant with a specific patient scenario:

```bash
python assistant.py --patient-file patient_agents.json --patient-index 0
```

This will:
- Load patient data from `patient_agents.json`
- Start an interactive conversation with the AI assistant
- Use voice input/output (if available)
- Apply verification checks and physician approval workflows

**Options:**
- `--patient-file`: Path to patient JSON file (default: `patient_agents.json`)
- `--patient-index`: Index of patient in the JSON file (default: 0)

### 2. Run Baseline Assistant (No Agent Handoffs)

For comparison without advanced agent features:

```bash
python base-assistant.py --patient-file patient_agents.json --patient-index 0
```

### 3. Run Full Simulation & Evaluation

Run automated simulations across all patient scenarios with comprehensive evaluation:

```bash
python simulation.py
```

**What this does:**
1. Loads all 41 patient scenarios from `patient_agents.json`
2. Simulates conversations between assistant and patient agents
3. Evaluates each conversation turn using 4-axis rubric (SAFE/CORRECT/OPTIMAL/EMPATHETIC)
4. Tracks protocol outcomes (medication progression, safety events, adherence)
5. Generates detailed evaluation reports
6. Creates comprehensive scores summary

**Output files** (in `eval_results/` directory):
- `<PATIENT_ID>_conversation.json` - Individual conversation logs with evaluations
- `simulation_summary.json` - Aggregate statistics across all conversations
- `all_scores_summary.json` - Comprehensive SCOE scores and distributions

**Simulation options:**
```bash
# Run with custom output directory
python simulation.py --output-dir my_results

# Use different agent file
python simulation.py --agent-file my_custom_agent.py

# Run specific patient scenarios only
# (Edit simulation.py to filter scenarios)
```

## 📁 Project Structure

```
cs224v-final-project-1/
├── assistant.py                 # Main assistant with agent handoffs
├── base-assistant.py           # Baseline assistant (no handoffs)
├── simulation.py               # Simulation & evaluation framework
├── patient_agents.json         # Patient scenarios (41 cases)
├── requirements.txt            # Python dependencies
│
├── prompts/                    # Agent instruction prompts
│   ├── assistantInstructions.py
│   ├── recommendationInstructions.py
│   ├── verificationAgentInstructions.py
│   ├── physicianApprovalVerificationInstructions.py
│   ├── judgeInstructions.py
│   └── protocolOutcomeInstructions.py
│
├── Knowledge/                  # Clinical knowledge base
│   ├── 01_ace_inhibitors.md
│   ├── 02_arbs.md
│   ├── 03_arni.md
│   ├── 04_aldosterone_antagonists.md
│   ├── 05_beta_blockers.md
│   ├── 06_hydralazine_isosorbide_dinitrate.md
│   ├── 07_sglt2_inhibitors.md
│   ├── 09_titration_parameters.md
│   └── 10_monitoring_guidelines.md
│
└── eval_results/               # Evaluation outputs (generated)
    ├── HF_CONV_003_conversation.json
    ├── simulation_summary.json
    └── all_scores_summary.json
```

## 📈 Understanding the Output

### Individual Conversation Files

Each `<PATIENT_ID>_conversation.json` contains:

```json
{
  "conversation_id": "HF_CONV_003",
  "patient_name": "HF_CONV_003",
  "total_turns": 10,
  "full_conversation_log": [...],  // Complete conversation history
  "rounds": [
    {
      "round_num": 1,
      "evaluation": {
        "safe": 5,           // Safety score (1-5)
        "correct": 4,        // Clinical correctness (1-5)
        "optimal": 4,        // Optimality of approach (1-5)
        "empathetic": 5,     // Empathy & communication (1-5)
        "weighted_score": 4.5,  // 0.35*safe + 0.30*correct + 0.20*optimal + 0.15*empathetic
        "auto_failures": []  // Automatic safety violations
      }
    }
  ],
  "protocol_outcome": {
    "medications_tracked": [
      {
        "medication_name": "Lisinopril",
        "starting_dose": "10mg daily",
        "final_dose": "20mg daily",
        "target_dose": "20mg daily"
      }
    ],
    "total_turns": 10,
    "safety_events": [],
    "adherence_issues": []
  }
}
```

### Comprehensive Scores Summary

`all_scores_summary.json` contains:

- **Aggregated SCOE scores**: Average, min, max across all evaluations
- **Individual scores**: Every round evaluation from all conversations
- **Score distributions**: Histogram of scores for each dimension
- **Summary statistics**: Total conversations, rounds, safety issues

**Key metrics:**
- **SAFE (35% weight)**: Vital sign monitoring, contraindication checks, safety protocols
- **CORRECT (30% weight)**: Guideline adherence, dosing accuracy, clinical reasoning
- **OPTIMAL (20% weight)**: Efficiency, long-term planning, titration strategy
- **EMPATHETIC (15% weight)**: Communication quality, patient engagement, support

## 🔬 Reproducing Results

### Full Evaluation Run

```bash
# 1. Ensure environment is set up
source venv/bin/activate
export OPENAI_API_KEY='your-api-key-here'

# 2. Run simulation (takes ~30-60 minutes for 41 scenarios)
python simulation.py

# 3. View results
cat eval_results/all_scores_summary.json | python -m json.tool
```

### Expected Outputs

After a successful run, you should see:
- **Terminal output**: Real-time progress, scores for each round
- **41 conversation files**: One per patient scenario
- **Summary files**: Aggregate statistics and comprehensive scores
- **Console summary**: Average SCOE scores printed at the end

### Typical Results Format

```
============================================================
EVALUATION SUMMARY
============================================================
Total Conversations: 41
Total Rounds Evaluated: 41
Average Scores:
  SAFE: 4.2/5
  CORRECT: 3.8/5
  OPTIMAL: 3.5/5
  EMPATHETIC: 4.5/5
  WEIGHTED: 4.0
```

## 🛠️ Customization

### Adding New Patient Scenarios

Edit `patient_agents.json`:

```json
{
  "patient_id": "HF_CONV_NEW",
  "medical_history": {
    "diagnosis": "Heart Failure with Reduced Ejection Fraction (HFrEF)",
    "medications": [
      {
        "name": "Medication Name",
        "type": "Drug Class",
        "current_dose": "Current dose",
        "target_dose": "Target dose"
      }
    ],
    "baseline_vitals": {
      "weight_lbs": 170,
      "blood_pressure": {"systolic": 120, "diastolic": 80},
      "heart_rate": 70,
      "oxygen_saturation": 98
    }
  },
  "conversation_turns": []  // Optional: pre-existing conversation
}
```

### Modifying Agent Instructions

Edit files in `prompts/` directory to customize agent behavior:
- `assistantInstructions.py` - Main assistant personality and guidelines
- `recommendationInstructions.py` - Medication recommendation logic
- `judgeInstructions.py` - Evaluation criteria and rubrics

### Adjusting Evaluation Criteria

Modify weights in `simulation.py`:

```python
weighted_score = (
    0.35 * safe_score +      # Safety weight
    0.30 * correct_score +   # Correctness weight
    0.20 * optimal_score +   # Optimality weight
    0.15 * empathetic_score  # Empathy weight
)
```

