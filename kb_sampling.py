# Sample features:
# slice_prob = [embb, urllc, mmtc]

# UEs number: arrival_rate - depature rate 
# Increasing UEs: arrival_rate = (default)1.5
# Decreasing UEs: depature_rate = (defaut)0.3 

# UEs pattern (walk, vehicle, stationary): pattern_prob = [wal, veh, sta]

# ?? change_direction_prob: moving behaviour

# Scenario: 
# slice_prob: 
# base [0.4, 0.3, 0.3]
# high slice_type_prob >= 0.7
# (4 cases)

# UEs pattern: base [0.5, 0.3, 0.2] | high [>0.7, >0.5, >0.5)] (4 cases)

# Number of UEs: sharp increase: ue_rate > 3 / sharp decrease: ue_rate < -2 / base (3 cases)

# reward weights: [qos, en, fair] | base = [2, 0.8, 0.5]
# Total: 48

# 10 simulate sample for each scenario: ~500 chunks

n_samples = 1000
samples = []

import random
from decimal import Decimal
def step_random(a, b, step):
    a = float(a)
    b = float(b)
    n = int((b - a)/step)
    rand_n = random.randint(0, n)
    return a + rand_n*step 

def decimal_round(n, prec):
    return Decimal(str(round(n,prec)))

def sample_case_ue_pattern(mode): #mode: 0, 1, 2, 3 - base, high wal, high veh, high sta
    if mode == 0:
        return [0.5, 0.3, 0.2]
    if mode == 1:
        wal = decimal_round(step_random(0.7, 0.9, 0.05),2)
        veh = decimal_round(step_random(0, 1-wal, 0.05),2)
        sta = 1 - wal - veh
    if mode == 2:
        veh = decimal_round(step_random(0.5, 1.0, 0.05),2)
        wal = decimal_round(step_random(0, 1-veh, 0.05),2)
        sta = 1 - veh - wal
    if mode == 3:
        sta = decimal_round(step_random(0.5, 1.0, 0.05),2)
        wal = decimal_round(step_random(0, 1-sta, 0.05),2)
        veh = 1 - sta - wal
    return [float(n) for n in [wal, veh, sta]]

def sample_case_slice_prob(mode): #0, 1, 2, 3: base, high embb, high urllc, high mmtc
    if mode == 0:
        return [0.4, 0.3, 0.3]
    if mode == 1:
        embb = decimal_round(step_random(0.7, 1, 0.05),2)
        urllc = decimal_round(step_random(0, 1-embb, 0.05),2)
        mmtc = 1 - embb - urllc
    if mode == 2:
        urllc = decimal_round(step_random(0.7, 1, 0.05),2)
        embb = decimal_round(step_random(0, 1-urllc, 0.05),2)
        mmtc = 1 - embb - urllc
    if mode == 3:
        mmtc = decimal_round(step_random(0.7, 1, 0.05),2)
        urllc = decimal_round(step_random(0, 1-mmtc, 0.05),2)
        embb = 1 - mmtc - urllc
    return [float(n) for n in [embb, urllc, mmtc]]

def sample_case_ue_num(mode): #0, 1, 2: base, sky-rocket, collapse
    if mode == 0:
        return 1.2
    if mode == 1:
        return 3
    if mode == 2:
        return -2
    

for i in range (0, n_samples):
    mode_1 = random.randint(0,3)
    if mode_1 == 0:
        state_slice = "Service usage balance"
    elif mode_1 == 1:
        state_slice = "Because the probability of embb >= 0.7, most users use embb"
    elif mode_1 == 2:
        state_slice = "Because the probability of urllc >= 0.7, most users use urllc"
    elif mode_1 == 3:
        state_slice = "Because the probability of mmtc >= 0.7, most users use mmtc"
    slice_probs = sample_case_slice_prob(mode_1)

    mode_2 = random.randint(0,3)
    if mode_1 == 0:
        state_user_pattern = "Usual users' moving pattern"
    elif mode_1 == 1:
        state_user_pattern = "Because the probability of users walking >= 0.7, most users walking"
    elif mode_1 == 2:
        state_user_pattern = "Because the probability of users using vehicle >= 0.5, most users using vehicle"
    elif mode_1 == 3:
        state_user_pattern = "Because the probability of users are stationary >= 0.5, most users are stationary"
    ue_patterns = sample_case_ue_pattern(mode_2)
    
    mode_3 = random.randint(0,2)
    if mode_3 == 0:
        state_user_num = "Usual trend in the change of user number"
    elif mode_3 == 1:
        state_user_num = "Because the rate of the change in user number >= 3, the number of user increase fast"
    elif mode_3 == 2:
        state_user_num = "Because the rate of the change in user number <= -2, the number of user decrease fast"
    ue_nums = sample_case_ue_num(random.randint(0,2))
    
    chunk_dict = {
        "slice": f"Probability of user using embb, urllc and mmtc is: {slice_probs[0]}, {slice_probs[1]}, {slice_probs[2]}",
        "ue_pattern": f"Probability of user walking, using vehicle and stationary is: {ue_patterns[0]}, {ue_patterns[1]}, {ue_patterns[2]}",
        "ue_arrival": f"The rate of the change in number of users is: {ue_nums}",
        "analyze": {
            "slice": state_slice,
            "ue_pattern": state_user_pattern,
            "ue_number": state_user_num
        },
        "action": "Reward weights for QoS, Energy and Fairness: 2, 0.8, 0.5",
        "reward": "1.5",
        "numeric_data": f"{[*slice_probs, *ue_patterns, ue_nums]}"
    }

    samples.append(chunk_dict)

import json
with open("sample_kb.jsonl", "w", encoding="utf8") as f:
    for row in samples:
        json.dump(row, f)
        f.write("\n")