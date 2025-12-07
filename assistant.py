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
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
import os
import threading
import sounddevice as sd
import json
import time
from websockets.sync.client import connect

SONIOX_WEBSOCKET_URL = "wss://stt-rt.soniox.com/transcribe-websocket"
SONIOX_API_KEY = os.environ.get("SONIOX_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY) if ELEVENLABS_API_KEY else None

'''
Code taken from Soniox documentation for recording and transcribing audio.
'''
class voiceCapture:
    def __init__(self):
        pass

    def record_audio(self, duration: int = 10):
        print("Press enter to stop recording")
        audio_buffer: list[bytes] = []
        stop_recording = threading.Event()

        def wait_for_enter():
            input()
            stop_recording.set()

        threading.Thread(target=wait_for_enter, daemon=True).start()

        with sd.RawInputStream(
            samplerate=16000,
            channels=1,
            dtype="int16",
            blocksize=1920,
        ) as stream:
            start_time = time.time()
            while not stop_recording.is_set() and (time.time() - start_time) < duration:
                data, _ = stream.read(1920)
                audio_buffer.append(bytes(data))
            if len(audio_buffer) == 0:
                return None
            return audio_buffer

    def transcribe_audio(self, audio_buffer):
        config = {
            "api_key": SONIOX_API_KEY,
            "model": "stt-rt-v3",
            "language_hints": ["en"],
            "enable_language_identification": True,
            "enable_speaker_diarization": False,
            "audio_format": "pcm_s16le",
            "sample_rate": 16000,
            "num_channels": 1,
            "enable_endpoint_detection": True,
        }

        transcription = ""

        with connect(SONIOX_WEBSOCKET_URL) as ws:
            ws.send(json.dumps(config))
            for chunk in audio_buffer:
                ws.send(chunk)
            ws.send("")

            while True:
                try:
                    message = ws.recv(timeout=2.0)
                except Exception:
                    break

                res = json.loads(message)

                for token in res.get("tokens", []):
                    if token.get("text") and token.get("is_final"):
                        transcription += token["text"]

                if res.get("finished"):
                    break

        return transcription.strip()

    def speak(self, text: str):
        audio = elevenlabs_client.text_to_speech.stream(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_flash_v2_5",
            output_format="mp3_44100_128",
        )
        stream(audio)


@function_tool
def checkNotEmergency (sbp: int | None = None, dbp: int | None = None, heartRate: int | None = None, oxygenSaturation: float | None = None, weight: float | None = None, symptoms: str | None = None, sideEffects: str | None = None, adherence: str | None = None, labs: str | None = None):
    if sbp and dbp and sbp < 90 or dbp < 50:
      return True
    if heartRate and heartRate < 50 or heartRate > 120:
      return True
    if oxygenSaturation and oxygenSaturation < 90:
      return True
    if weight and weight < 100 or weight > 200:
      return True

@function_tool
def physicianApproval(recommendation: str):
    return True

@function_tool
async def verifyPhysicianApproval(recommendation: str, patient_vitals: str = "", patient_labs: str = "", approved: bool = True):
    """
    After receiving physician approval, verify that the approved recommendation 
    does not violate any contraindications or HOLD criteria.
    
    This runs AFTER physicianApproval returns True.
    """
    from agents import Agent, Runner
    
    verification_agent = Agent(
        name="Physician Approval Verification Agent",
        instructions=verificationAgentInstructions,
        model="gpt-4o-mini"
    )
    
    verification_prompt = f"""
The physician has approved the following recommendation:

RECOMMENDATION:
{recommendation}

PATIENT VITALS:
{patient_vitals}

PATIENT LABS:
{patient_labs}

PHYSICIAN DECISION: {"APPROVED" if approved else "NOT APPROVED"}

Please verify if this approved recommendation violates any contraindications or HOLD criteria from the protocol.

Respond with:
1. VERIFIED - if the approval is safe and appropriate
2. CONCERN - if there are potential safety issues
3. REJECT - if the approval clearly violates protocol and should not proceed

Provide detailed reasoning for your assessment.
"""
    
    result = await Runner.run(verification_agent, verification_prompt)
    return str(result.final_output) if result.final_output else "Unable to verify"


class AssistantOrchestrator:
    def __init__(self, scenario_str: str):
        self.verification_agent = Agent(
            name="Verification Agent",
            instructions=verificationAgentInstructions,
            model="gpt-4o-mini"
        )
        self.arb_checker = Agent(
            name="ARB Checker",
            instructions=ARB_CHECKER,
            model="gpt-4o-mini"
        )
        self.arni_checker = Agent(
            name="ARNI Checker",
            instructions=ARNI_CHECKER,
            model="gpt-4o-mini"
        )
        self.aldosterone_antagonist_checker = Agent(
            name="Aldosterone Antagonist Checker",
            instructions=ALDOSTERONE_ANTAGONIST_CHECKER,
            model="gpt-4o-mini"
        )
        self.beta_blocker_checker = Agent(
            name="Beta Blocker Checker",
            instructions=BETA_BLOCKER_CHECKER,
            model="gpt-4o-mini"
        )
        self.sgc_checker = Agent(
            name="SGC Checker",
            instructions=SGC_CHECKER,
            model="gpt-4o-mini"
        )
        self.sglt2_checker = Agent(
            name="SGLT2 Checker",
            instructions=SGLT2_CHECKER,
            model="gpt-4o-mini"
        )
        self.hydralazine_checker = Agent(
            name="Hydralazine Checker",
            instructions=HYDRAZINE_CHECKER,
            model="gpt-4o-mini"
        )
        self.arb_checker = Agent(
            name="ARB Checker",
            instructions=ARB_CHECKER,
            model="gpt-4o-mini"
        )
        self.recommendation_agent = Agent(
            name="Recommendation Agent",
            instructions=recommendationAgentInstructions,
            model="gpt-4o-mini",
            tools=[
                checkNotEmergency, 
                self.arb_checker.as_tool(
                    tool_description="Check if the patient's condition violates any of the contraindications or HOLD criteria for ARBs.", 
                    tool_name="check_arb"
                ), 
                self.arni_checker.as_tool(
                    tool_description="Check if the patient's condition violates any of the contraindications or HOLD criteria for ARNI.", 
                    tool_name="check_arni"
                ), 
                self.aldosterone_antagonist_checker.as_tool(
                    tool_description="Check if the patient's condition violates any of the contraindications or HOLD criteria for aldosterone antagonists.", 
                    tool_name="check_aldosterone_antagonist"
                ), 
                self.beta_blocker_checker.as_tool(
                    tool_description="Check if the patient's condition violates any of the contraindications or HOLD criteria for beta blockers.", 
                    tool_name="check_beta_blocker"
                ), 
                self.sgc_checker.as_tool(
                    tool_description="Check if the patient's condition violates any of the contraindications or HOLD criteria for SGC.", 
                    tool_name="check_sgc"
                ), 
                self.sglt2_checker.as_tool(
                    tool_description="Check if the patient's condition violates any of the contraindications or HOLD criteria for SGLT2.", 
                    tool_name="check_sglt2"
                ), 
                self.hydralazine_checker.as_tool(
                    tool_description="Check if the patient's condition violates any of the contraindications or HOLD criteria for hydralazine.", 
                    tool_name="check_hydralazine"
                ), 
                physicianApproval,
                verifyPhysicianApproval
            ],
        )
        combined_instructions = f"{scenario_str}\n\n{assistantInstructions}"
        self.assistant_agent = Agent(
            name="Assistant Agent",
            instructions=combined_instructions,
            model="gpt-4o-mini",
            tools=[
                self.recommendation_agent.as_tool(
                    tool_name="call_recommendation_agent",
                    tool_description=(
                        "Given a structured summary of the patient's symptoms, vitals, "
                        "side effects, and adherence, generate a titration recommendation."
                    ),
                ),
                # self.verification_agent.as_tool(
                #     tool_name="call_verification_agent",
                #     tool_description=(
                #         "Given a structured summary of the patient's symptoms, vitals, "
                #         "side effects, and adherence, verify if the titration recommendation is correct."
                #     ),
                # ),
            ],
        )
        self.voiceCapture = voiceCapture()
    async def run(self):
        conversation: List[TResponseInputItem] = []
        current_agent = self.assistant_agent

        # Ask ONCE at the start
        choice = input(
            "Hi! I'm Titus, your heart failure titration assistant.\n"
            "Type 'v' if you want to speak. Or you can just type too: "
        )

        if choice.lower() in ["quit", "q", "exit"]:
            return

        use_voice = (choice == "v")
        if use_voice:
            self.voiceCapture.speak("Hi! We have the medical team on the line for your titration check in. Are you ready")

        # If user typed text (not 'v'), treat that as the first patient message
        initial_text_message = None
        if not use_voice:
            initial_text_message = choice

        while True:
            if use_voice:
                # VOICE MODE: record every turn
                audio_buffer = self.voiceCapture.record_audio(duration=30)
                if not audio_buffer:
                    print("No audio captured, please try again.")
                    continue
                transcription = self.voiceCapture.transcribe_audio(audio_buffer)
                patient_input = transcription
                print(f"Patient: {patient_input}")
            else:
                # TEXT MODE: first turn uses the initial text, then we prompt each time
                if initial_text_message is not None:
                    patient_input = initial_text_message
                    initial_text_message = None  # only use once
                else:
                    patient_input = input("You: ")
                    if patient_input.lower() in ["quit", "q", "exit"]:
                        break

            conversation.append({"role": "user", "content": patient_input})

            agentResponse = await Runner.run(current_agent, conversation)
            conversation = agentResponse.to_input_list()
            current_agent = agentResponse.last_agent

            print("Titus: " + agentResponse.final_output)
            if use_voice:
                self.voiceCapture.speak(agentResponse.final_output)

async def main():
    scenario_str = """
     "clinical_scenario": {
        "patient_name": "Patient",
        "medications": [
          {
            "name": "Losartan",
            "type": "ARB",
            "current": "50mg daily",
            "target": "100mg daily",
            "stage": "mid"
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
            "current": "25mg daily",
            "target": "50mg daily",
            "stage": "early"
          },
          {
            "name": "Dapagliflozin",
            "type": "SGLT2 Inhibitor",
            "current": "5mg daily",
            "target": "10mg daily",
            "stage": "early"
          },
          {
            "name": "Furosemide",
            "type": "Loop Diuretic",
            "current": "40mg daily",
            "target": "dose adjustment as needed",
            "stage": "maintenance"
          }
        ],
        "therapy_complexity": "complete_therapy",
        "titration_stage": "early_optimization"
      },
  """

    assistant_agent = AssistantOrchestrator(scenario_str)
    await assistant_agent.run()


if __name__ == "__main__":
    asyncio.run(main())