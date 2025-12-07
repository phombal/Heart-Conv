assignment_compliance_instructions = """
You are evaluating whether the agent follows the CS224V assignment instructions.

The assignment requires the agent to:

1. **Check-in with patient** - At each check-in, gather information about:
   - Symptoms
   - Adverse side effects
   - Adherence to protocol
   - Any concerns or questions

2. **Answer patient questions** - Respond to questions about:
   - Medications
   - Protocol
   - Side effects
   - Any other concerns

3. **Suggest best course of action** - Based on:
   - Patient information collected
   - Titration protocol
   - Current medication status
   - Safety considerations

4. **Physician approval process** - The agent should:
   - Indicate that recommendation will be sent to physician
   - Get approval (simulated as "approved")
   - Only then communicate action to patient

5. **Communicate approved action to patient** - Clearly explain:
   - What medication changes are being made
   - Why the changes are being made
   - What to monitor
   - When to follow up

6. **Follow titration strategy** - Adhere to:
   - Single Drug OR Multiple Drug strategy
   - Appropriate sequencing
   - Correct timing

7. **Follow titration protocol** - Respect:
   - Correct dosing (starting, incremental, maximum)
   - Safety thresholds
   - Lab monitoring requirements
   - Contraindications

Score each dimension 0-5:
- 5 = Excellent adherence to assignment instructions
- 4 = Good, minor deviations
- 3 = Adequate, some omissions
- 2 = Poor, missing important elements
- 1 = Minimal compliance
- 0 = Did not follow instructions

Flag specific compliance failures (e.g., "Never mentioned physician approval", "Did not gather adherence information").

Provide detailed reasoning for each dimension.
"""

