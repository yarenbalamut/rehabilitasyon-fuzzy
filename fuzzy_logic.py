# fuzzy_logic.py

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Girdi tanımları
hr = ctrl.Antecedent(np.arange(0, 201, 1), 'Heart Rate')
rr = ctrl.Antecedent(np.arange(0, 41, 1), 'Respiratory Rate')
spo2 = ctrl.Antecedent(np.arange(0, 101, 1), 'SpO2')
sbp = ctrl.Antecedent(np.arange(0, 201, 1), 'Systolic BP')
temp = ctrl.Antecedent(np.round(np.arange(30, 42.01, 0.1), 1), 'Temperature')

# Çıktı tanımları
urgency = ctrl.Consequent(np.arange(0, 101, 1), 'Urgency')
stabilization_index = ctrl.Consequent(np.arange(0, 101, 1), 'Stabilization Index')

# Üyelik fonksiyonları - Girişler
hr['low'] = fuzz.trapmf(hr.universe, [0, 0, 50, 61])
hr['normal'] = fuzz.trimf(hr.universe, [59, 75, 101])
hr['high'] = fuzz.trapmf(hr.universe, [99, 120, 200, 200])

rr['low'] = fuzz.trapmf(rr.universe, [0, 0, 10, 13])
rr['normal'] = fuzz.trimf(rr.universe, [11, 16, 21])
rr['high'] = fuzz.trapmf(rr.universe, [19, 25, 40, 40])

spo2['low'] = fuzz.trapmf(spo2.universe, [0, 0, 85, 91])
spo2['normal'] = fuzz.trapmf(spo2.universe, [89, 95, 100, 100])

sbp['low'] = fuzz.trapmf(sbp.universe, [0, 0, 85, 90])
sbp['normal'] = fuzz.trimf(sbp.universe, [89, 105, 121])
sbp['high'] = fuzz.trapmf(sbp.universe, [119, 140, 200, 200])

temp['low'] = fuzz.trapmf(temp.universe, [30, 30, 35, 36.1])
temp['normal'] = fuzz.trimf(temp.universe, [35.9, 36.75, 37.6])
temp['high'] = fuzz.trapmf(temp.universe, [37.4, 38.5, 42, 42])

# Üyelik fonksiyonları - Çıktılar
urgency['low'] = fuzz.trimf(urgency.universe, [0, 0, 33])
urgency['medium'] = fuzz.trimf(urgency.universe, [25, 50, 75])
urgency['high'] = fuzz.trimf(urgency.universe, [67, 100, 100])

stabilization_index['short'] = fuzz.trimf(stabilization_index.universe, [0, 0, 33])
stabilization_index['medium'] = fuzz.trimf(stabilization_index.universe, [25, 50, 75])
stabilization_index['long'] = fuzz.trimf(stabilization_index.universe, [67, 100, 100])

# Kural listesi - toplam 62 kural
rules = [
    ctrl.Rule(hr['low'] & rr['low'], urgency['high']),
    ctrl.Rule(hr['low'] & spo2['low'], urgency['high']),
    ctrl.Rule(hr['low'] & sbp['low'], urgency['high']),
    ctrl.Rule(hr['low'] & temp['low'], urgency['medium']),
    ctrl.Rule(hr['low'] & rr['normal'], urgency['medium']),
    ctrl.Rule(hr['low'] & spo2['normal'], urgency['medium']),
    ctrl.Rule(hr['low'] & sbp['normal'], urgency['medium']),
    ctrl.Rule(hr['low'] & temp['normal'], urgency['low']),
    ctrl.Rule(hr['low'] & temp['high'], urgency['medium']),

    ctrl.Rule(hr['normal'] & rr['low'], urgency['medium']),
    ctrl.Rule(hr['normal'] & rr['normal'], urgency['low']),
    ctrl.Rule(hr['normal'] & rr['high'], urgency['medium']),
    ctrl.Rule(hr['normal'] & spo2['low'], urgency['medium']),
    ctrl.Rule(hr['normal'] & spo2['normal'], urgency['low']),
    ctrl.Rule(hr['normal'] & sbp['low'], urgency['medium']),
    ctrl.Rule(hr['normal'] & sbp['normal'], urgency['low']),
    ctrl.Rule(hr['normal'] & sbp['high'], urgency['medium']),
    ctrl.Rule(hr['normal'] & temp['low'], urgency['medium']),
    ctrl.Rule(hr['normal'] & temp['normal'], urgency['low']),
    ctrl.Rule(hr['normal'] & temp['high'], urgency['medium']),

    ctrl.Rule(hr['high'] & rr['low'], urgency['high']),
    ctrl.Rule(hr['high'] & rr['normal'], urgency['high']),
    ctrl.Rule(hr['high'] & rr['high'], urgency['high']),
    ctrl.Rule(hr['high'] & spo2['low'], urgency['high']),
    ctrl.Rule(hr['high'] & spo2['normal'], urgency['medium']),
    ctrl.Rule(hr['high'] & sbp['low'], urgency['high']),
    ctrl.Rule(hr['high'] & sbp['normal'], urgency['medium']),
    ctrl.Rule(hr['high'] & sbp['high'], urgency['high']),
    ctrl.Rule(hr['high'] & temp['low'], urgency['high']),
    ctrl.Rule(hr['high'] & temp['normal'], urgency['medium']),
    ctrl.Rule(hr['high'] & temp['high'], urgency['high']),

    ctrl.Rule(spo2['low'] & sbp['low'], urgency['high']),
    ctrl.Rule(spo2['low'] & temp['low'], stabilization_index['long']),
    ctrl.Rule(spo2['low'] & temp['high'], urgency['high']),
    ctrl.Rule(spo2['normal'] & sbp['normal'], urgency['low']),
    ctrl.Rule(spo2['normal'] & temp['normal'], urgency['low']),
    ctrl.Rule(spo2['normal'] & sbp['high'], urgency['medium']),

    ctrl.Rule(rr['low'] & temp['low'], stabilization_index['long']),
    ctrl.Rule(rr['high'] & temp['high'], stabilization_index['long']),
    ctrl.Rule(rr['normal'] & temp['normal'], stabilization_index['short']),
    ctrl.Rule(rr['high'] & spo2['low'], urgency['high']),
    ctrl.Rule(rr['high'] & sbp['low'], urgency['high']),
    ctrl.Rule(rr['low'] & sbp['low'], stabilization_index['long']),
    ctrl.Rule(temp['high'] & sbp['high'], urgency['high']),
    ctrl.Rule(temp['high'] & hr['high'], stabilization_index['long']),
    ctrl.Rule(temp['low'] & sbp['low'], stabilization_index['long']),
    ctrl.Rule(temp['normal'] & hr['normal'], stabilization_index['short']),

    ctrl.Rule(spo2['low'] & hr['low'], stabilization_index['long']),
    ctrl.Rule(spo2['low'] & sbp['low'], stabilization_index['long']),
    ctrl.Rule(spo2['low'] & rr['low'], stabilization_index['long']),
    ctrl.Rule(spo2['low'] & temp['low'], stabilization_index['long']),
    ctrl.Rule(spo2['low'] & temp['high'], stabilization_index['long']),
    ctrl.Rule(spo2['normal'] & rr['normal'], stabilization_index['short']),
    ctrl.Rule(spo2['normal'] & hr['normal'], stabilization_index['short']),
    ctrl.Rule(spo2['normal'] & temp['normal'], stabilization_index['short']),
    ctrl.Rule(spo2['normal'] & sbp['normal'], stabilization_index['short']),

    ctrl.Rule(temp['high'] & sbp['normal'], stabilization_index['medium']),
    ctrl.Rule(temp['low'] & sbp['normal'], stabilization_index['medium']),
    ctrl.Rule(temp['normal'] & hr['high'], stabilization_index['medium']),
    ctrl.Rule(temp['normal'] & rr['high'], stabilization_index['medium']),
    ctrl.Rule(temp['normal'] & sbp['high'], stabilization_index['medium']),
    ctrl.Rule(temp['normal'] & hr['low'], stabilization_index['medium']),
]

# Kontrol sistemi tanımı
assessment_ctrl = ctrl.ControlSystem(rules)
# Educational prototype: these indices are not validated medical measurements.
INPUT_RANGES = {
    'Heart Rate': (0.0, 200.0),
    'Respiratory Rate': (0.0, 40.0),
    'SpO2': (0.0, 100.0),
    'Systolic BP': (0.0, 200.0),
    'Temperature': (30.0, 42.0),
}


def evaluate_patient(hr_val, rr_val, spo2_val, sbp_val, temp_val):
    """Return two 0-100 fuzzy indices, not a clinical score or time estimate."""
    import math
    values = {
        'Heart Rate': hr_val,
        'Respiratory Rate': rr_val,
        'SpO2': spo2_val,
        'Systolic BP': sbp_val,
        'Temperature': temp_val,
    }
    for name, value in values.items():
        try:
            numeric_value = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f'{name}: geçerli bir sayı girin.') from exc
        lower, upper = INPUT_RANGES[name]
        if not math.isfinite(numeric_value) or not lower <= numeric_value <= upper:
            raise ValueError(f'{name}: {lower:g} ile {upper:g} arasında bir değer girin.')
        values[name] = numeric_value

    # Create a separate simulation for each input set.
    simulation = ctrl.ControlSystemSimulation(assessment_ctrl)
    for name, value in values.items():
        simulation.input[name] = value

    try:
        simulation.compute()
        return (
            float(simulation.output['Urgency']),
            float(simulation.output['Stabilization Index']),
        )
    except (ValueError, KeyError, AssertionError) as exc:
        raise ValueError(
            'Bu girdi kombinasyonu mevcut kural tabanıyla hesaplanamadı. '
            'Değerleri ve model kapsamını kontrol edin.'
        ) from exc
