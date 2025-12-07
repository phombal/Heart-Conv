"""
BASE ASSISTANT - Simplified Baseline Agent

This is a minimal baseline implementation for comparison against the full multi-agent system.

Key Differences from assistant.py:
- NO agent handoffs (no Recommendation Agent, Verification Agent)
- NO tool calling (no checkNotEmergency, no medication checker agents)
- NO detailed titration protocol knowledge
- NO complex contraindication checking
- SIMPLIFIED instructions (basic clinical reasoning only)

Purpose: Establish a performance baseline to measure the value-add of:
1. Multi-agent orchestration
2. Detailed protocol encoding
3. Automated safety checks
4. Structured recommendation/verification workflow
"""

from agents import Agent, Runner, TResponseInputItem
import asyncio
from typing import List
import json

from prompts.baseAssistantInstructions import assistantInstructions

class AssistantOrchestrator:
    """
    Base assistant without any agent handoffs or tool calls.
    Single agent that handles all logic directly with simplified instructions.
    """
    def __init__(self, scenario_str: str):
        # Create a single assistant agent with scenario context
        combined_instructions = f"{scenario_str}\n\n{assistantInstructions}"
        
        self.assistant_agent = Agent(
            name="Base Assistant Agent",
            instructions=combined_instructions,
            model="gpt-4o-mini",
            tools=[]  # No tools - agent handles everything directly
        )
    
    async def run_with_history(self, conversation_history: List[TResponseInputItem]):
        """
        Run the assistant with existing conversation history.
        Continues the conversation from where it left off.
        
        Args:
            conversation_history: List of previous conversation turns
        """
        conversation: List[TResponseInputItem] = conversation_history.copy()
        current_agent = self.assistant_agent
        
        # Display the conversation history
        print("=== Previous Conversation History ===")
        for turn in conversation:
            role = turn.get("role", "")
            content = turn.get("content", "")
            if role == "user":
                print(f"Patient: {content}")
            elif role == "assistant":
                print(f"Assistant: {content}")
        print("=== Continuing Conversation ===\n")
        
        while True:
            patient_input = input("Patient: (use 'quit' to exit): ")
            if patient_input == "quit":
                break
            conversation.append({"role": "user", "content": patient_input})

            agentResponse = await Runner.run(current_agent, conversation)
            conversation = agentResponse.to_input_list()
            current_agent = agentResponse.last_agent

            print("Assistant: " + agentResponse.final_output)
    
    async def run(self):
        """Interactive run method for manual testing"""
        conversation: List[TResponseInputItem] = []
        current_agent = self.assistant_agent
        
        while True:
            patient_input = input("Patient: (use 'quit' to exit): ")
            if patient_input == "quit":
                break
            conversation.append({"role": "user", "content": patient_input})

            agentResponse = await Runner.run(current_agent, conversation)
            conversation = agentResponse.to_input_list()
            current_agent = agentResponse.last_agent

            print("Assistant: " + agentResponse.final_output)


def load_patient_scenario(patient_data: dict) -> tuple[str, List[TResponseInputItem]]:
    """
    Convert patient data from the new JSON format to scenario string and conversation history.
    
    Args:
        patient_data: Dictionary containing patient_id, medical_history, and conversation_turns
        
    Returns:
        Tuple of (scenario_str, conversation_history)
    """
    medical_history = patient_data.get("medical_history", {})
    
    # Build scenario string from medical history
    scenario_parts = [
        f"Patient ID: {patient_data.get('patient_id', 'Unknown')}",
        f"Diagnosis: {medical_history.get('diagnosis', 'Unknown')}",
    ]
    
    # Add comorbidities if present
    comorbidities = medical_history.get("comorbidities", [])
    if comorbidities:
        scenario_parts.append(f"Comorbidities: {', '.join(comorbidities)}")
    
    # Add medications
    medications = medical_history.get("medications", [])
    if medications:
        scenario_parts.append("\nMedications:")
        for med in medications:
            scenario_parts.append(
                f"  - {med.get('name')} ({med.get('type')}): "
                f"Current dose: {med.get('current_dose')}, "
                f"Target dose: {med.get('target_dose')}"
            )
    
    # Add baseline vitals
    baseline_vitals = medical_history.get("baseline_vitals", {})
    if baseline_vitals:
        scenario_parts.append("\nBaseline Vitals:")
        if baseline_vitals.get("weight_lbs") is not None:
            scenario_parts.append(f"  - Weight: {baseline_vitals['weight_lbs']} lbs")
        bp = baseline_vitals.get("blood_pressure", {})
        if bp:
            scenario_parts.append(
                f"  - Blood Pressure: {bp.get('systolic')}/{bp.get('diastolic')} mmHg"
            )
        if baseline_vitals.get("heart_rate") is not None:
            scenario_parts.append(f"  - Heart Rate: {baseline_vitals['heart_rate']} bpm")
        if baseline_vitals.get("oxygen_saturation") is not None:
            scenario_parts.append(f"  - Oxygen Saturation: {baseline_vitals['oxygen_saturation']}%")
    
    scenario_str = "\n".join(scenario_parts)
    
    # Convert conversation_turns to conversation history
    conversation_history: List[TResponseInputItem] = []
    conversation_turns = patient_data.get("conversation_turns", [])
    
    for turn in conversation_turns:
        role = turn.get("role", "")
        content = turn.get("content", "")
        
        # Map patient role to user, agent role to assistant
        if role == "patient":
            conversation_history.append({"role": "user", "content": content})
        elif role == "agent":
            conversation_history.append({"role": "assistant", "content": content})
    
    return scenario_str, conversation_history


async def main():
    """Test the base assistant with a sample scenario"""
    import sys
    
    # Check if a JSON file path was provided
    if len(sys.argv) > 1:
        json_file_path = sys.argv[1]
        patient_index = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        
        # Load patient data from JSON file
        with open(json_file_path, 'r') as f:
            patient_data_list = json.load(f)
        
        if not isinstance(patient_data_list, list):
            print("Error: JSON file must contain a list of patient scenarios")
            return
        
        if patient_index >= len(patient_data_list):
            print(f"Error: Patient index {patient_index} is out of range (0-{len(patient_data_list)-1})")
            return
        
        patient_data = patient_data_list[patient_index]
        scenario_str, conversation_history = load_patient_scenario(patient_data)
        
        print(f"Loading scenario for: {patient_data.get('patient_id')}")
        print(f"Starting with {len(conversation_history)} existing conversation turns\n")
    else:
        # Default scenario for testing
        scenario_str = """
Patient ID: TEST_001
Diagnosis: Heart Failure with Reduced Ejection Fraction (HFrEF)

Medications:
  - Losartan (ARB): Current dose: 25mg daily, Target dose: 100mg daily
  - Metoprolol Succinate (Beta-Blocker): Current dose: 100mg daily, Target dose: 200mg daily

Baseline Vitals:
  - Blood Pressure: 120/75 mmHg
  - Heart Rate: 68 bpm
        """
        conversation_history = []
        print("No JSON file provided. Using default test scenario.\n")
        print("Usage: python base-assistant.py <path_to_json> [patient_index]")
        print("Example: python base-assistant.py patient_agents.json 0\n")

    assistant_agent = AssistantOrchestrator(scenario_str)
    
    # If there's existing conversation history, inject it into the agent
    if conversation_history:
        await assistant_agent.run_with_history(conversation_history)
    else:
        await assistant_agent.run()


if __name__ == "__main__":
    asyncio.run(main())


