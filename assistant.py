from agents import (
    Agent,
    HandoffOutputItem,
    ItemHelpers,
    MessageOutputItem,
    Runner,
    ToolCallItem,
    ToolCallOutputItem,
    TResponseInputItem,
    function_tool,
    handoff,
    trace,
)
import asyncio
from typing import List

from prompts.verificationAgentInstructions import verificationAgentInstructions
from prompts.recommendationInstructions import recommendationAgentInstructions
from prompts.assistantInstructions import assistantInstructions


class AssistantOrchestrator:
    def __init__(self, scenario_str: str):
        self.recommendation_agent = Agent(
            name="Recommendation Agent",
            instructions=recommendationAgentInstructions,
        )

        self.verification_agent = Agent(
            name="Verification Agent",
            instructions=verificationAgentInstructions,
        )

        combined_instructions = f"{scenario_str}\n\n{assistantInstructions}"
        self.assistant_agent = Agent(
            name="Assistant Agent",
            instructions=combined_instructions,
            tools=[
                self.recommendation_agent.as_tool(
                    tool_name="call_recommendation_agent",
                    tool_description=(
                        "Given a structured summary of the patient's symptoms, vitals, "
                        "side effects, and adherence, generate a titration recommendation."
                    ),
                ),
                self.verification_agent.as_tool(
                    tool_name="call_verification_agent",
                    tool_description=(
                        "Given a structured summary of the patient's symptoms, vitals, "
                        "side effects, and adherence, verify if the titration recommendation is correct."
                    ),
                ),
            ],
        )
    
    async def run(self):
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

            print(agentResponse.final_output)


async def main():
    # # Default clinical scenario based on HF_CONV_001 (Abigail Baker) from all_conversations.json
    # default_medications = [
    #     Medication(
    #         name="Losartan",
    #         type="ARB",
    #         current="50mg daily",
    #         target="100mg daily",
    #         stage="mid",
    #     ),
    #     Medication(
    #         name="Metoprolol Succinate",
    #         type="Beta-Blocker",
    #         current="100mg daily",
    #         target="200mg daily",
    #         stage="advanced",
    #     ),
    #     Medication(
    #         name="Eplerenone",
    #         type="Aldosterone Antagonist",
    #         current="25mg daily",
    #         target="50mg daily",
    #         stage="early",
    #     ),
    #     Medication(
    #         name="Dapagliflozin",
    #         type="SGLT2 Inhibitor",
    #         current="5mg daily",
    #         target="10mg daily",
    #         stage="early",
    #     ),
    #     Medication(
    #         name="Furosemide",
    #         type="Loop Diuretic",
    #         current="40mg daily",
    #         target="dose adjustment as needed",
    #         stage="maintenance",
    #     ),
    # ]

    # default_scenario = ClinicalScenario(
    #     name="Abigail Baker",
    #     education_level="College",
    #     medical_literacy="Moderate",
    #     description="Understands some medical concepts, asks informed questions",
    #     medications=default_medications,
    #     therapy_complexity="complete_therapy",
    #     titration_state="early_optimization",
    # )

    # Example: scenario passed in as a JSON string (can be built dynamically per patient)
    scenario_str = """
    "patient_name": "Ethan Bailey",
    "medications": [
      {
        "name": "Losartan",
        "type": "ARB",
        "current": "25mg daily",
        "target": "100mg daily",
        "stage": "early"
      },
      {
        "name": "Metoprolol Succinate",
        "type": "Beta-Blocker",
        "current": "100mg daily",
        "target": "200mg daily",
        "stage": "advanced"
      },
      {
        "name": "Eplerenone",
        "type": "Aldosterone Antagonist",
        "current": "50mg daily",
        "target": "100mg daily",
        "stage": "mid"
      },
      {
        "name": "Dapagliflozin",
        "type": "SGLT2 Inhibitor",
        "current": "5mg daily",
        "target": "10mg daily",
        "stage": "early"
      },
      {
        "name": "Hydrochlorothiazide",
        "type": "Thiazide Diuretic",
        "current": "25mg daily",
        "target": "dose adjustment as needed",
        "stage": "maintenance"
      }
    ],
    "therapy_complexity": "complete_therapy",
    "titration_stage": "early_optimization"
  """

    assistant_agent = AssistantOrchestrator(scenario_str)
    await assistant_agent.run()


if __name__ == "__main__":
    asyncio.run(main())