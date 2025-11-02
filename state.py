from pydantic import BaseModel, field_validator, Field
from typing import List, Optional, Literal, Dict

class VitalsEntry(BaseModel):
    weight: float = Field(description="Patient's weight in pounds")
    weight_change: float = Field(description="Weight change in pounds from the previous check or week")
    weight_trend: str = Field(description= "YOU MUST CHOOSE FROM ONE OF THE FOLLOWING: INCREASING, DECREASING, STABLE")
    SBP: int = Field(description= "Systolic blood pressure")
    DBP: int = Field(description="disystolic blood pressure")
    oxygen_saturation: float = Field(description="oxygen saturation")


class PatientState(BaseModel):
    vitals: List[VitalsEntry] = []
    side_effects: List = []
    adherence: str = ""

    def add_vitals(self, vitals):
        print(f"Adding vitals {vitals}")
        self.vitals = vitals
    





