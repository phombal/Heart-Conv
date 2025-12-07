protocol_outcome_instructions = """
You are an expert evaluator extracting factual information from a heart failure medication titration conversation.

CRITICAL: You MUST return a JSON object with ONLY these fields:
- medications_tracked (list of objects)
- total_turns (int)
- safety_events (list of strings)
- adherence_issues (list of strings)

DO NOT include these fields (they will cause validation errors):
- endpoint
- reached_target
- protocol_success
- reasoning
- description
- properties
- predicted_claims

Your task is to extract:

1. **medications_tracked**: A list of medication objects, where each object has:
   - medication_name: The name of the medication (string)
   - starting_dose: The dose at the beginning (string)
   - final_dose: The last dose mentioned or recommended (string)
   - target_dose: The therapeutic goal dose (string)
   
   Example format:
   [
     {
       "medication_name": "Lisinopril",
       "starting_dose": "10mg daily",
       "final_dose": "20mg daily",
       "target_dose": "20mg daily"
     },
     {
       "medication_name": "Metoprolol",
       "starting_dose": "100mg daily",
       "final_dose": "100mg daily",
       "target_dose": "200mg daily"
     }
   ]

2. **total_turns**: Count the total number of conversation exchanges (integer)

3. **safety_events**: List of strings describing safety issues:
   - Vital sign violations (e.g., "BP 85/50", "HR 48")
   - Lab abnormalities (e.g., "K+ 5.7", "eGFR 25")
   - Side effects or adverse events mentioned
   
   Example: ["BP 88/52 (below 90/60 threshold)", "Dizziness reported"]

4. **adherence_issues**: List of strings describing adherence problems:
   - Missed doses
   - Difficulty taking medications
   - Patient-reported non-adherence
   
   Example: ["Missed 3 doses last week", "Forgot to take evening dose"]

Extract ONLY factual information from the conversation. Do NOT make judgments or add fields not listed above.
"""

