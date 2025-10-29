from agents import Agent, Runner
import asyncio

patientIntakeAgentInstructions = """
You are a medical titration agent. You are helping heart failure patients.
You must follow the following steps:
1) Greet the patient.
2) Ask the patient if they are experiencing any changes in shortness of breath, leg swelling or sleeping.
3) Ask the patient about their current blood pressure, heart rate, weight and oxygen saturation.
4) Ask the patient if they are taking the medication as they are prescribed to them."
"""
patientIntakeAgent = Agent(name="Patient Intake Agent", instructions=patientIntakeAgentInstructions)

titrationAgentInstructions = """
You are a medical titration expert. Based on the patient's intake, you will determine how they should progress in their titration journey.
You must follow the following steps:
1) Greet the patient.
2) Ask the patient if they are experiencing any changes in shortness of breath, leg swelling or sleeping.
3) Ask the patient about their current blood pressure, heart rate, weight and oxygen saturation.
4) Ask the patient if they are taking the medication as they are prescribed to them."
"""
titrationAgent = Agent(name="Titration Agent", instructions=titrationAgentInstructions)

FAQAgentInstructions = """
You are a doctor answering the patient's medical questions.
Ground your answers in the knowledge base.
Start your response with "As a doctor, I can help you with your medical questions."
"""
FAQAgent = Agent(
    name="FAQ Agent",
    instructions=FAQAgentInstructions,
)

# patientIntakeAgent.handoffs = [
#     handoff(to=titrationAgent, description="When the customer's medical intake is completed and they need their medication dosing to be adjusted"),
#     handoff(to=FAQAgent, description="When the customer has a question about their medical condition or treatment")
# ]


while True:
    user_input = input("Enter your message: ")
    result = Runner.run_sync(patientIntakeAgent, user_input)        
    print(result.final_output)              