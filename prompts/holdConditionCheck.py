ACEI = """
Verify the patient's current medical profile doesn't violate any of these contraindications or HOLD criteria. Don't be cautious - there should be a clear violation
of the contraindication or HOLD criteria for the medication for you to suggest that the patient discontinue, reduce the dose, or continue.

**Contraindications:** If the patient displays any of this, stop taking the medication.

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

For each of the ACEI medications that the patient is taking (Enalapril, Lisinopril, Ramipril, Captopril), return the following summary:
- [Medication Name] | [Condition Violated] | [Discontinue, Reduce Dose, Continue]
"""
ARB_CHECKER = """
Verify the patient's current medical profile doesn't violate any of these contraindications or HOLD criteria. Don't be cautious - there should be a clear violation
of the contraindication or HOLD criteria for the medication for you to suggest that the patient discontinue, reduce the dose, or continue.
**Contraindications:** If the patient displays any of this, stop taking the medication.

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

For each of the ARB medications that the patient is taking (Losartan, Valsartan, Candesartan), return the following summary:
- [Medication Name] | [Condition Violated] | [Discontinue, Reduce Dose, Continue]
"""

ARNI_CHECKER = """
Verify the patient's current medical profile doesn't violate any of these contraindications or HOLD criteria. Don't be cautious - there should be a clear violation
of the contraindication or HOLD criteria for the medication for you to suggest that the patient discontinue, reduce the dose, or continue.

**Contraindications:** If the patient displays any of this, stop taking the medication.

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

For each of the ARNI medications that the patient is taking (Sacubitril/Valsartan), return the following summary:
- [Medication Name] | [Condition Violated] | [Discontinue, Reduce Dose, Continue]
"""

ALDOSTERONE_ANTAGONIST_CHECKER = """
Verify the patient's current medical profile doesn't violate any of these contraindications or HOLD criteria. Don't be cautious - there should be a clear violation
of the contraindication or HOLD criteria for the medication for you to suggest that the patient discontinue, reduce the dose, or continue.

**Contraindications:** If the patient displays any of this, stop taking the medication.

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

For each of the aldosterone antagonist medications that the patient is taking (Spironolactone, Eplerenone), return the following summary:
- [Medication Name] | [Condition Violated] | [Discontinue, Reduce Dose, Continue]
"""
BETA_BLOCKER_CHECKER = """
Verify the patient's current medical profile doesn't violate any of these contraindications or HOLD criteria. Don't be cautious - there should be a clear violation
of the contraindication or HOLD criteria for the medication for you to suggest that the patient discontinue, reduce the dose, or continue.

**Contraindications:** If the patient displays any of this, stop taking the medication.

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

For each of the beta blocker medications that the patient is taking (Carvedilol, Metoprolol Succinate, Bisoprolol), return the following summary:
- [Medication Name] | [Condition Violated] | [Discontinue, Reduce Dose, Continue]
"""

HYDRAZINE_CHECKER = """
Verify the patient's current medical profile doesn't violate any of these contraindications or HOLD criteria. Don't be cautious - there should be a clear violation
of the contraindication or HOLD criteria for the medication for you to suggest that the patient discontinue, reduce the dose, or continue.

**Contraindications:** If the patient displays any of this, stop taking the medication.
- SBP <85–90 mmHg symptomatic
- PDE-5 inhibitor use
- Recent MI (<48 hr)
- Drug-induced lupus

**Hold or Discontinue if:**
- Hypotension or orthostasis
- Drug-induced lupus
- Severe headache
- Tachycardia >110–120 bpm

For each of the hydralazine medications that the patient is taking (Hydralazine, Isosorbide Dinitrate, Fixed-Dose Combination (BiDil)), return the following summary:
- [Medication Name] | [Condition Violated] | [Discontinue, Reduce Dose, Continue]
"""

SGLT2_CHECKER = """
Verify the patient's current medical profile doesn't violate any of these contraindications or HOLD criteria. Don't be cautious - there should be a clear violation
of the contraindication or HOLD criteria for the medication for you to suggest that the patient discontinue, reduce the dose, or continue.

### Contraindications If the patient displays any of this, stop taking the medication.
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

For each of the SGLT2 medications that the patient is taking (Dapagliflozin, Empagliflozin, Sotagliflozin), return the following summary:
- [Medication Name] | [Condition Violated] | [Discontinue, Reduce Dose, Continue]
"""

SGC_CHECKER = """
Verify the patient's current medical profile doesn't violate any of these contraindications or HOLD criteria. Don't be cautious - there should be a clear violation
of the contraindication or HOLD criteria for the medication for you to suggest that the patient discontinue, reduce the dose, or continue.
### Contraindications If the patient displays any of this, stop taking the medication.
- PDE-5 inhibitor use
- Pregnancy
- Severe hepatic impairment (Child-Pugh C)

### Hold / Discontinue If
- SBP <90 mmHg symptomatic
- Symptomatic hypotension
- Concurrent PDE-5 inhibitor need
- Pregnancy
- Worsening anemia

For each of the SGC medications that the patient is taking (Vericiguat), return the following summary:
- [Medication Name] | [Condition Violated] | [Discontinue, Reduce Dose, Continue]
"""