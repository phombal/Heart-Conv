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
from prompts.holdConditionCheck import ARB_CHECKER, ARNI_CHECKER, ALDOSTERONE_ANTAGONIST_CHECKER, BETA_BLOCKER_CHECKER, SGC_CHECKER, SGLT2_CHECKER, HYDRAZINE_CHECKER

@function_tool
def checkNotEmergency (sbp: int | None = None, dbp: int | None = None, heartRate: int | None = None, oxygenSaturation: float | None = None, weight: float | None = None, symptoms: str | None = None, sideEffects: str | None = None, adherence: str | None = None, labs: str | None = None):
    print("CALLING TOOL")
    if sbp and dbp and sbp < 90 or dbp < 50:
      return True
    if heartRate and heartRate < 50 or heartRate > 120:
      return True
    if oxygenSaturation and oxygenSaturation < 95:
      return True
    if weight and weight < 100 or weight > 200:
      return True

class AssistantOrchestrator:
    def __init__(self, scenario_str: str):
        

        self.verification_agent = Agent(
            name="Verification Agent",
            instructions=verificationAgentInstructions,
        )

        self.arb_checker = Agent(
            name="ARB Checker",
            instructions=ARB_CHECKER,
        )
        self.arni_checker = Agent(
            name="ARNI Checker",
            instructions=ARNI_CHECKER,
        )
        self.aldosterone_antagonist_checker = Agent(
            name="Aldosterone Antagonist Checker",
            instructions=ALDOSTERONE_ANTAGONIST_CHECKER,
        )
        self.beta_blocker_checker = Agent(
            name="Beta Blocker Checker",
            instructions=BETA_BLOCKER_CHECKER,
        )
        self.sgc_checker = Agent(
            name="SGC Checker",
            instructions=SGC_CHECKER,
        )
        self.sglt2_checker = Agent(
            name="SGLT2 Checker",
            instructions=SGLT2_CHECKER,
        )
        self.hydralazine_checker = Agent(
            name="Hydralazine Checker",
            instructions=HYDRAZINE_CHECKER,
        )
        self.arb_checker = Agent(
            name="ARB Checker",
            instructions=ARB_CHECKER,
        )
        self.recommendation_agent = Agent(
            name="Recommendation Agent",
            instructions=recommendationAgentInstructions,
            tools=[checkNotEmergency, self.arb_checker.as_tool(tool_description="Check if the patient's condition violates any of the contraindications or HOLD criteria for ARBs.", tool_name="check_arb"), self.arni_checker.as_tool(tool_description="Check if the patient's condition violates any of the contraindications or HOLD criteria for ARNI.", tool_name="check_arni"), self.aldosterone_antagonist_checker.as_tool(tool_description="Check if the patient's condition violates any of the contraindications or HOLD criteria for aldosterone antagonists.", tool_name="check_aldosterone_antagonist"), self.beta_blocker_checker.as_tool(tool_description="Check if the patient's condition violates any of the contraindications or HOLD criteria for beta blockers.", tool_name="check_beta_blocker"), self.sgc_checker.as_tool(tool_description="Check if the patient's condition violates any of the contraindications or HOLD criteria for SGC.", tool_name="check_sgc"), self.sglt2_checker.as_tool(tool_description="Check if the patient's condition violates any of the contraindications or HOLD criteria for SGLT2.", tool_name="check_sglt2"), self.hydralazine_checker.as_tool(tool_description="Check if the patient's condition violates any of the contraindications or HOLD criteria for hydralazine.", tool_name="check_hydralazine")],
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