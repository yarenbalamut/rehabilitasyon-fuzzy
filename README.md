# Fuzzy Logic-Based Vital Signs Assessment

**Rule-based decision-support concept and desktop prototype** built using Python, scikit-fuzzy, Tkinter and Matplotlib.

This educational project explores how fuzzy inference can combine five vital-sign inputs into two **illustrative indices on a 0–100 scale**.

> **Research / educational prototype only.** The indices are not clinically validated. Do not use for diagnosis, triage, patient monitoring, treatment, or any medical decision.

## Highlights

- Five input variables: heart rate, respiratory rate, oxygen saturation (SpO₂), systolic blood pressure, and body temperature.
- **62 IF–THEN fuzzy inference rules** (verified in source).
- Overlapping membership functions for modeled input ranges, including cutoff and boundary values.
- Two numerical outputs: **Urgency Index** and **Stabilization Index**, both 0–100.
- Tkinter desktop interface with range validation and Matplotlib visualization.
- Independent simulation per evaluation to avoid mixing states.

**Important:** The *Stabilization Index* is a model output, **not** an estimate of stabilization time in minutes, hours, or days. No real-world accuracy, prediction quality or medical benefit has been established.

## Approach

The application uses Mamdani-style fuzzy inference with the `scikit-fuzzy` control system. Membership functions turn each numerical input into linguistic sets, the original 62 pairwise rules aggregate corresponding outcomes, and defuzzification produces relative model indices. A graphical interface allows educational experimentation with input scenarios.

The following represent software-accepted ranges, **not validated clinical thresholds**:

| Input | Model range |
| --- | --- |
| Heart rate | 0–200 beats/min |
| Respiratory rate | 0–40 breaths/min |
| SpO₂ | 0–100% |
| Systolic blood pressure | 0–200 mmHg |
| Temperature | 30–42 °C |

## Quick start

Requires Python 3.10+, Tkinter and a desktop graphical environment.

```bash
git clone https://github.com/yarenbalamut/rehabilitasyon-fuzzy.git
cd rehabilitasyon-fuzzy
python -m pip install -r requirements.txt
python main.py
```

Regression tests (after installing dependencies):

```bash
python -m unittest discover -s tests -v
```

## Files

- `fuzzy_logic.py` — fuzzy variables, 62 rules, independent model evaluation, input validation.
- `main.py` — Tkinter desktop interface and Matplotlib visualization.
- `tests/test_fuzzy_logic.py` — tests for sample inputs, previous boundary gaps and invalid values.

## Scope and limitations

This is a **rule-based fuzzy-logic prototype, not a trained machine-learning model**. It has no clinical dataset, medical expert validation, clinical outcome labels, calibration, real-world pilot, or regulatory review. Its rules and scores are illustrative rather than medically tested. The project demonstrates Python programming, fuzzy modeling, prototyping, input validation and data visualization.

Originally developed as a learning project; later refined for clearer output labels, validation and visualization.
