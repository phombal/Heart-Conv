ACEI = """
Verify the patient's current medical profile doesn't violate any of these contraindications or HOLD criteria. Don't be cautious - only if there is a clear violation should you tell
the patient that they cannot take their medications.
**Contraindications:**

* History of angioedema with ACE-I  
* Bilateral renal artery stenosis  
* Pregnancy  
* Concomitant use with aliskiren in patients with diabetes  
* Concurrent or recent (\<48 hours) use of neprilysin inhibitor

**Hold or Discontinue if:**

* **Potassium \>5.5 mEq/L** (hold; may resume at lower dose if K+ normalizes)  
* **Creatinine increase \>30% from baseline** (hold; reassess in 1-2 weeks)  
* **eGFR \<20-30 mL/min** (use caution; consider dose reduction or discontinuation)  
* **Symptomatic hypotension** with SBP \<80-90 mmHg  
* **Angioedema** (discontinue permanently)  
* **Hyperkalemia persisting \>6.0 mEq/L** despite intervention (discontinue)

"""
ARB_CHECKER = """
Verify the patient's current medical profile doesn't violate any of these contraindications or HOLD criteria. Don't be cautious - only if there is a clear violation should you tell
the patient that they cannot take their medications.
**Contraindications:**

* History of angioedema with ARB  
* Bilateral renal artery stenosis  
* Pregnancy  
* Concomitant use with aliskiren in patients with diabetes  
* Concurrent or recent (\<48 hours) use of neprilysin inhibitor

**Hold or Discontinue if:**

* **Potassium \>5.5 mEq/L** (hold; may resume at lower dose if K+ normalizes)  
* **Creatinine increase \>30% from baseline** (hold; reassess in 1-2 weeks)  
* **eGFR \<20-30 mL/min** (use caution; consider dose reduction or discontinuation)  
* **Symptomatic hypotension** with SBP \<80-90 mmHg  
* **Angioedema** (discontinue permanently)  
* **Hyperkalemia persisting \>6.0 mEq/L** despite intervention (discontinue)
"""

ARNI_CHECKER = """
Verify the patient's current medical profile doesn't violate any of these contraindications or HOLD criteria. Don't be cautious - only if there is a clear violation should you tell
the patient that they cannot take their medications.*Contraindications:**

* History of angioedema with ACE-I, ARB, or neprilysin inhibitor  
* Concurrent use with ACE-I (must wait 48 hours after last ACE-I dose)  
* Pregnancy  
* Severe hepatic impairment (Child-Pugh Class C)

**Hold or Discontinue if:**

* **Potassium \>5.5 mEq/L** (hold; may resume at lower dose if K+ normalizes)  
* **Creatinine increase \>30% from baseline** (hold; reassess in 1-2 weeks)  
* **eGFR \<20 mL/min** (use with extreme caution or consider discontinuation)  
* **Symptomatic hypotension** with SBP \<80-90 mmHg  
* **Angioedema** (discontinue permanently)  
* **Hyperkalemia persisting \>6.0 mEq/L** despite intervention (discontinue)
"""

ALDOSTERONE_ANTAGONIST_CHECKER = """
Verify the patient's current medical profile doesn't violate any of these contraindications or HOLD criteria. Don't be cautious - only if there is a clear violation should you tell
the patient that they cannot take their medications.
Aldosterone Antagonists**

**Contraindications:**

* **Baseline potassium \>5.0 mEq/L**  
* **eGFR \<30 mL/min**  
* Concurrent use of strong CYP3A4 inhibitors (eplerenone)  
* Addison's disease or hyperkalemia

**Hold or Discontinue if:**

* **Potassium \>5.5 mEq/L** (hold; may resume at lower dose if K+ 4.5-5.0 mEq/L)  
* **Potassium \>6.0 mEq/L** (discontinue)  
* **Creatinine increase \>30% from baseline or eGFR drops to \<30 mL/min** (hold or discontinue)  
* **Severe gynecomastia or breast tenderness** (consider switching spironolactone to eplerenone)  
* **Symptomatic hypotension**

"""
BETA_BLOCKER_CHECKER = """
Verify the patient's current medical profile doesn't violate any of these contraindications or HOLD criteria. Don't be cautious - only if there is a clear violation should you tell
the patient that they cannot take their medications.

**Contraindications:**

* Symptomatic bradycardia or heart rate \<50 bpm  
* Second or third-degree AV block (without pacemaker)  
* Sick sinus syndrome (without pacemaker)  
* Severe decompensated heart failure requiring inotropic support  
* Severe asthma or active bronchospasm  
* Cardiogenic shock

**Hold or Discontinue if:**

* **Heart rate \<50 bpm** (hold or reduce dose)  
* **Heart rate \<45 bpm** (hold; consider discontinuation if persistent)  
* **Symptomatic bradycardia** (reduce dose or discontinue)  
* **Second or third-degree AV block** develops (discontinue)  
* **SBP \<80-85 mmHg with symptoms** (hold or reduce dose)  
* **Acute decompensated heart failure** requiring IV diuretics/inotropes (hold temporarily)  
* **Severe bronchospasm** (discontinue)

"""

HYDRAZINE_CHECKER = """
Verify the patient's current medical profile doesn't violate any of these contraindications or HOLD criteria. Don't be cautious - only if there is a clear violation should you tell
the patient that they cannot take their medications.

**Contraindications:**
- SBP <85–90 mmHg symptomatic
- PDE-5 inhibitor use
- Recent MI (<48 hr)
- Drug-induced lupus

**Hold or Discontinue if:**
- Hypotension or orthostasis
- Drug-induced lupus
- Severe headache
- Tachycardia >110–120 bpm

"""

SGLT2_CHECKER = """
Verify the patient's current medical profile doesn't violate any of these contraindications or HOLD criteria. Don't be cautious - only if there is a clear violation should you tell
the patient that they cannot take their medications.

### Contraindications
- eGFR <20 (dapagliflozin, empagliflozin)
- eGFR <25 (sotagliflozin)
- Type 1 diabetes
- DKA history
- Dialysis

### Hold / Discontinue If
- eGFR below threshold
- DKA or euglycemic DKA
- Severe dehydration
- Recurrent UTI or genital infection
- Fournier’s gangrene
- AKI (temporary hold)

"""

SGC_CHECKER = """
Verify the patient's current medical profile doesn't violate any of these contraindications or HOLD criteria. Don't be cautious - only if there is a clear violation should you tell
the patient that they cannot take their medications.
### Contraindications
- PDE-5 inhibitor use
- Pregnancy
- Severe hepatic impairment (Child-Pugh C)

### Hold / Discontinue If
- SBP <90 mmHg symptomatic
- Symptomatic hypotension
- Concurrent PDE-5 inhibitor need
- Pregnancy
- Worsening anemia

"""