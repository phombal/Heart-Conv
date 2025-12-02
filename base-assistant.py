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
            tools=[]  # No tools - agent handles everything directly
        )
    
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

            print(agentResponse.final_output)


async def main():
    """Test the base assistant with a sample scenario"""
    scenario_str = """
    "patient_name": "Test Patient",
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
      }
    ],
    "therapy_complexity": "dual_therapy",
    "therapy_goal": "optimization"
  """

    assistant_agent = AssistantOrchestrator(scenario_str)
    await assistant_agent.run()


if __name__ == "__main__":
    asyncio.run(main())


