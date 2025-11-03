# simulation.py
import asyncio
import json
import os
from pathlib import Path
from agents import Agent, Runner
from dotenv import load_dotenv; load_dotenv()

"""
Define the HF assistant agent locally (matches Patient Intake Agent in titration-agent.py)
"""
patientIntakeAgentInstructions = """
You are a medical titration agent. You are helping heart failure patients.
You must follow the following steps:
1) Greet the patient.
2) Ask the patient if they are experiencing any changes in shortness of breath, leg swelling or sleeping.
3) Ask the patient about their current blood pressure, heart rate, weight and oxygen saturation.
4) Ask the patient if they are taking the medication as they are prescribed to them.
"""

agent = Agent(name="Patient Intake Agent", instructions=patientIntakeAgentInstructions)

def build_patient_simulator_agent(scenario):
    """
    Build a patient-simulator Agent (OpenAI Agents SDK) from a conversation scenario.
    The agent roleplays the patient and outputs the next patient message given the assistant's last turn.
    """
    patient_profile = scenario.get("patient_profile", {})
    clinical_scenario = scenario.get("clinical_scenario", {})
    conversation_goal = scenario.get("conversation_goal", "")

    instructions = f"""
You are roleplaying as the patient named {clinical_scenario.get('patient_name', 'Patient')}.

PATIENT PROFILE:
- Education Level: {patient_profile.get('education_level', 'Unknown')}
- Medical Literacy: {patient_profile.get('medical_literacy', 'Unknown')}
- Communication Style: {patient_profile.get('description', '')}

CURRENT MEDICATION REGIMEN:
"""
    for med in clinical_scenario.get('medications', []):
        instructions += f"- {med.get('name', 'Unknown')} ({med.get('type', 'Unknown')}): current {med.get('current', 'Unknown')}, target {med.get('target', 'Unknown')}\n"

    instructions += f"""
CLINICAL CONTEXT:
- Therapy Complexity: {clinical_scenario.get('therapy_complexity', 'Unknown')}
- Titration Stage: {clinical_scenario.get('titration_stage', 'Unknown')}

CONVERSATION GOAL:
{conversation_goal}

HOW TO RESPOND:
- Always speak as the patient in first person.
- Keep responses brief, natural, and consistent with the education level and medical literacy.
- If given the assistant's last message, answer it directly; otherwise start the conversation with a natural opening consistent with the goal.
- Include concrete vitals/symptoms only if implied by the goal; do not fabricate unrelated details.
"""

    return Agent(name="Patient Simulator", instructions=instructions)

async def generate_patient_input(patient_agent: Agent, assistant_last_message: str | None = None):
    """
    Use the Agents SDK to generate the patient's next message.
    If assistant_last_message is None, generate the opening patient message.
    """
    prompt = assistant_last_message or "Begin the conversation as the patient."
    result = await Runner.run(patient_agent, prompt)
    return str(result.final_output) if result.final_output else ""

async def main():
    # Load conversation scenarios (supports both list and { conversations: [...] } formats)
    try:
        conv_path = Path(__file__).parent / 'conversations.json'
        if not conv_path.exists():
            print(f"conversations.json not found at {conv_path}")
            return
        raw = conv_path.read_text(encoding='utf-8').strip()
        print(f"Loaded conversations.json from {conv_path} (bytes={len(raw)})")
        if not raw:
            print("conversations.json is empty. Add scenarios and try again.")
            return
        loaded = json.loads(raw)
        if isinstance(loaded, dict) and "conversations" in loaded:
            scenarios = loaded["conversations"]
        elif isinstance(loaded, list):
            scenarios = loaded
        else:
            print("conversations.json has an unexpected format. Expected a list or an object with 'conversations'.")
            return
    except json.JSONDecodeError as e:
        print(f"Failed to parse conversations.json: {e}")
        return

    # Surface API key visibility to this process (helps diagnose env issues)
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY is not set in this process environment. The Agents SDK will fail to call models.")

    # Process each conversation scenario
    for scenario in scenarios:
        conversation_id = scenario.get('id', 'unknown')
        print(f"\n{'='*80}")
        print(f"Starting conversation: {conversation_id}")
        print(f"{'='*80}\n")
        
        # Build a patient-simulator agent for this scenario
        patient_agent = build_patient_simulator_agent(scenario)

        # Initialize conversation history (starts empty for first turn)
        conversation_history = []
        
        # Generate multiple turns of conversation (adjust number as needed)
        num_turns = 20  # Number of patient-AI exchanges per conversation
        
        for turn in range(num_turns):
            try:
                # For the first turn, generate initial patient input with no assistant message
                # For subsequent turns, generate based on the assistant's last response
                if turn == 0:
                    patient_input = await generate_patient_input(patient_agent, None)
                else:
                    last_assistant_msg = conversation_history[-1]["content"] if conversation_history and conversation_history[-1]["role"] == "assistant" else ""
                    patient_input = await generate_patient_input(patient_agent, last_assistant_msg)
                
                print(f"\n[Turn {turn + 1}] Patient: {patient_input}")
                
                # Get AI agent response
                result = await Runner.run(agent, patient_input)
                ai_response = str(result.final_output) if result.final_output else ""
                
                print(f"[Turn {turn + 1}] HF-Agent: {ai_response}\n")
                
                # Update conversation history
                conversation_history.append({"role": "user", "content": patient_input})
                conversation_history.append({"role": "assistant", "content": ai_response})
                
                # Add a small delay to avoid rate limiting
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"Error in turn {turn + 1}: {e}")
                break
        
        print(f"\n{'='*80}")
        print(f"Completed conversation: {conversation_id}")
        print(f"{'='*80}\n")

if __name__ == "__main__":
    asyncio.run(main())
