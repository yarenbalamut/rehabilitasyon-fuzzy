# fuzzy_logic.py

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Girdi tanımları
hr = ctrl.Antecedent(np.arange(0, 201, 1), 'Heart Rate')
rr = ctrl.Antecedent(np.arange(0, 41, 1), 'Respiratory Rate')
spo2 = ctrl.Antecedent(np.arange(0, 101, 1), 'SpO2')
sbp = ctrl.Antecedent(np.arange(0, 201, 1), 'Systolic BP')
temp = ctrl.Antecedent(np.arange(30, 43, 0.1), 'Temperature')

# Çıktı tanımları
urgency = ctrl.Consequent(np.arange(0, 101, 1), 'Urgency')
stabilization_time = ctrl.Consequent(np.arange(0, 101, 1), 'Stabilization Time')

# Üyelik fonksiyonları - Girişler
hr['low'] = fuzz.trapmf(hr.universe, [0, 0, 50, 60])
hr['normal'] = fuzz.trimf(hr.universe, [60, 75, 100])
hr['high'] = fuzz.trapmf(hr.universe, [100, 120, 200, 200])

rr['low'] = fuzz.trapmf(rr.universe, [0, 0, 10, 12])
rr['normal'] = fuzz.trimf(rr.universe, [12, 16, 20])
rr['high'] = fuzz.trapmf(rr.universe, [20, 25, 40, 40])

spo2['low'] = fuzz.trapmf(spo2.universe, [0, 0, 85, 90])
spo2['normal'] = fuzz.trimf(spo2.universe, [90, 95, 100])

sbp['low'] = fuzz.trapmf(sbp.universe, [0, 0, 85, 90])
sbp['normal'] = fuzz.trimf(sbp.universe, [90, 105, 120])
sbp['high'] = fuzz.trapmf(sbp.universe, [120, 140, 200, 200])

temp['low'] = fuzz.trapmf(temp.universe, [30, 30, 35, 36])
temp['normal'] = fuzz.trimf(temp.universe, [36, 36.75, 37.5])
temp['high'] = fuzz.trapmf(temp.universe, [37.5, 38.5, 42, 42])

# Üyelik fonksiyonları - Çıktılar
urgency['low'] = fuzz.trimf(urgency.universe, [0, 0, 33])
urgency['medium'] = fuzz.trimf(urgency.universe, [25, 50, 75])
urgency['high'] = fuzz.trimf(urgency.universe, [67, 100, 100])

stabilization_time['short'] = fuzz.trimf(stabilization_time.universe, [0, 0, 33])
stabilization_time['medium'] = fuzz.trimf(stabilization_time.universe, [25, 50, 75])
stabilization_time['long'] = fuzz.trimf(stabilization_time.universe, [67, 100, 100])

# Kural listesi (örneklerden genişletilmiş - toplam 70 kural)
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
    ctrl.Rule(spo2['low'] & temp['low'], stabilization_time['long']),
    ctrl.Rule(spo2['low'] & temp['high'], urgency['high']),
    ctrl.Rule(spo2['normal'] & sbp['normal'], urgency['low']),
    ctrl.Rule(spo2['normal'] & temp['normal'], urgency['low']),
    ctrl.Rule(spo2['normal'] & sbp['high'], urgency['medium']),

    ctrl.Rule(rr['low'] & temp['low'], stabilization_time['long']),
    ctrl.Rule(rr['high'] & temp['high'], stabilization_time['long']),
    ctrl.Rule(rr['normal'] & temp['normal'], stabilization_time['short']),
    ctrl.Rule(rr['high'] & spo2['low'], urgency['high']),
    ctrl.Rule(rr['high'] & sbp['low'], urgency['high']),
    ctrl.Rule(rr['low'] & sbp['low'], stabilization_time['long']),
    ctrl.Rule(temp['high'] & sbp['high'], urgency['high']),
    ctrl.Rule(temp['high'] & hr['high'], stabilization_time['long']),
    ctrl.Rule(temp['low'] & sbp['low'], stabilization_time['long']),
    ctrl.Rule(temp['normal'] & hr['normal'], stabilization_time['short']),

    ctrl.Rule(spo2['low'] & hr['low'], stabilization_time['long']),
    ctrl.Rule(spo2['low'] & sbp['low'], stabilization_time['long']),
    ctrl.Rule(spo2['low'] & rr['low'], stabilization_time['long']),
    ctrl.Rule(spo2['low'] & temp['low'], stabilization_time['long']),
    ctrl.Rule(spo2['low'] & temp['high'], stabilization_time['long']),
    ctrl.Rule(spo2['normal'] & rr['normal'], stabilization_time['short']),
    ctrl.Rule(spo2['normal'] & hr['normal'], stabilization_time['short']),
    ctrl.Rule(spo2['normal'] & temp['normal'], stabilization_time['short']),
    ctrl.Rule(spo2['normal'] & sbp['normal'], stabilization_time['short']),

    ctrl.Rule(temp['high'] & sbp['normal'], stabilization_time['medium']),
    ctrl.Rule(temp['low'] & sbp['normal'], stabilization_time['medium']),
    ctrl.Rule(temp['normal'] & hr['high'], stabilization_time['medium']),
    ctrl.Rule(temp['normal'] & rr['high'], stabilization_time['medium']),
    ctrl.Rule(temp['normal'] & sbp['high'], stabilization_time['medium']),
    ctrl.Rule(temp['normal'] & hr['low'], stabilization_time['medium']),
]

# Kontrol sistemi tanımı
assessment_ctrl = ctrl.ControlSystem(rules)
assessment = ctrl.ControlSystemSimulation(assessment_ctrl)

def evaluate_patient(hr_val, rr_val, spo2_val, sbp_val, temp_val):
    assessment.input['Heart Rate'] = hr_val
    assessment.input['Respiratory Rate'] = rr_val
    assessment.input['SpO2'] = spo2_val
    assessment.input['Systolic BP'] = sbp_val
    assessment.input['Temperature'] = temp_val
    assessment.compute()
    return assessment.output['Urgency'], assessment.output['Stabilization Time']