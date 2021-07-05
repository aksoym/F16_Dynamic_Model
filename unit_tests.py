from update_motion import update_motion
import time
import numpy as np
from aero_model_to_replace import coefficient
import pickle


def update_motion_unit_test(function):

    #Arguments.

    state = {"Vt": 100, "beta": 0, "alpha": 0, "p": 0, "q": 0, "r": 0, "x": 0, "y": 0, "z": 10000, "phi": 0,
             "theta": 0, "psi": 0}

    plane_matrix = np.array([
        1, 0, 0,
        0, 1, 0,
        0, 0, 1,
        0, 0, 10000
    ])

    plane_speed_vector = np.array([
        101, 1.32, 5
    ])

    deltaE = 0
    deltaA = 0
    deltaR = 0

    thrust_lever = 0.9
    begin = time.time()
    result = function(plane_matrix, plane_speed_vector, state, deltaE, deltaA, deltaR, thrust_lever)
    end = time.time()


    print(result)
    print(f'Time elapsed in function runtime {end - begin} s')

def aero_coefficient_unit_test(function, label):
    point = (0, 0, 0)
    print(function(label, point))
    return None

with open('data/ParsedAeroDataBPs.pkl', 'rb') as f:
    breakpoints = pickle.load(f)


print(breakpoints['CY'].keys())
