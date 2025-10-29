# simulation.py
import asyncio
import json
import re
from agents import Runner
from agent import agent

async def main():
    data = []

    with open('all_conversations.json', 'r') as f:
        data = json.load(f)

    for data_entry in data["conversations"]:
        full_convo = data_entry['conversation']
        patient_inputs = re.findall(r"\*\*Patient\*\*:\s*(.*?)\s*(?=\n\*\*AI Assistant\*\*|\n---|$)", full_convo, re.DOTALL)
        patient_inputs = [line.strip() for line in patient_inputs]

        for input_text in patient_inputs:
            print(f"\nPatient: {input_text}")
            result = await Runner.run(agent, input_text) 
            print(f"HF-Agent: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
