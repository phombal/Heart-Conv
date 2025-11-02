from agents import (
    Agent,
    HandoffOutputItem,
    ItemHelpers,
    MessageOutputItem,
    RunContextWrapper,
    Runner,
    ToolCallItem,
    ToolCallOutputItem,
    TResponseInputItem,
    function_tool,
    handoff,
    trace,
    function_tool
)
import asyncio
from state import PatientState, VitalsEntry
from typing import List

state = PatientState()

@function_tool
def createVitalEntry(weight: float, weight_change: float, weight_trend: str, SBP: int, DBP: int, oxygen_saturation: float):
    """
    Create and return a structured object only after you have access to all the required information.
    weight_trend can only be: INCREASING, DECREASING, or STABLE
    """
    print("creating entry")
    vitals = VitalsEntry(
        weight=weight,
        weight_change=weight_change,
        weight_trend=weight_trend,
        SBP=SBP,
        DBP=DBP,
        oxygen_saturation=oxygen_saturation
    )
    print(vitals)
    state.add_vitals(vitals)
    return vitals
   
@function_tool
def createSideEffectsList(side_effects: List[str]):
    side_effects = side_effects
    return side_effects

VitalCollectingToolAgentInstructions = """
You MUST collect all of the following information before you call the createVitalEntry tool:
- weight (in pounds)
- weight_change (change from previous measurement in pounds)
- weight_trend (must be INCREASING, DECREASING, or STABLE). Do not ask the patient for this information. Infer it based on the weight change they say.
- SBP (systolic blood pressure)
- DBP (diastolic blood pressure)  
- oxygen_saturation (as a percentage)

Ask questions one at a time. Be conversational and friendly and nice.
If information is missing and they refuse to give it, remind them that you cannot help them unless they provide information.
"""

VitalCollectingToolAgent = Agent(name="Vitals Collection Agent", instructions=VitalCollectingToolAgentInstructions, tools=[createVitalEntry])

MainAgentInstructions = """
You are a medical assisstant collecting information and making a recommendation to a physician to help them titrate medical dosing. You need to collect information
about the patient's symptoms, their vitals, and their overall adherence.
(1): ask the patient about any new symptoms they are experiencing. Concatenate these symptoms in a list and then call the CreateSymptomList tool to store it.
(2): Call VitalCollectingTool agent to get information about patient vitals
(3): ask them whether or not they are adhering to their medical protocol. Ask them if they've taken their medicine and if they've explicitly missed any doses.
(4): summarize the adherence information in one sentence fragment. 

"""

MainAgent = Agent(name = "Physician Assistant Agent", instructions=MainAgentInstructions, tools=[VitalCollectingToolAgent.as_tool(tool_name="VitalCollectingToolAgent", tool_description="Collect information about the patient's vitals"), createVitalEntry])

#code taken from example agents in OpenAI Agents SDK documentation
async def main():
    input_items: list[TResponseInputItem] = []
    # context = AirlineAgentContext()

    # Normally, each input from the user would be an API request to your app, and you can wrap the request in a trace()
    # Here, we'll just use a random UUID for the conversation ID

    while True:
        user_input = input("Enter your message: ")
        # with trace("Customer service", group_id=conversation_id):
        input_items.append({"content": user_input, "role": "user"})
        result = await Runner.run(MainAgent, input_items)

        for new_item in result.new_items:
            agent_name = new_item.agent.name
            if isinstance(new_item, MessageOutputItem):
                print(f"{agent_name}: {ItemHelpers.text_message_output(new_item)}")
            elif isinstance(new_item, HandoffOutputItem):
                print(
                    f"Handed off from {new_item.source_agent.name} to {new_item.target_agent.name}"
                )
            elif isinstance(new_item, ToolCallItem):
                print(f"{agent_name}: Calling a tool")
            elif isinstance(new_item, ToolCallOutputItem):
                print(f"{agent_name}: Tool call output: {new_item.output}")
            else:
                print(f"{agent_name}: Skipping item: {new_item.__class__.__name__}")
        input_items = result.to_input_list()
        current_agent = result.last_agent


if __name__ == "__main__":
    asyncio.run(main())