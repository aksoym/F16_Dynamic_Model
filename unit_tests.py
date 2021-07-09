from update_motion import update_motion
import time
import numpy as np
from aero_model_to_replace import get_aero_forces, get_aero_force_coefficients, get_aero_moment_coefficients, _coefficient
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl


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

with open('data/ParsedAeroDataValues.pkl', 'rb') as f:
    breakpoints = pickle.load(f)


density = 1.225
velocity = 200
alpha, beta = 20, 0
p, q, r = 0, 0, 0
deltaE, deltaA, deltaR, deltaLEF, deltaSB = 0, 0, 0, 0, 0


cl_values = []
alpha_list = np.arange(0, 40)
deltaE_list = [0, 10, 25]

for alpha in alpha_list:
    coef = get_aero_force_coefficients(velocity, alpha, beta, p, q, r, deltaE, deltaA, deltaR, deltaLEF, deltaSB)[3]
    cl_values.append(coef)


def plot():
    plt.figure(figsize=(6, 8))
    plt.plot(alpha_list, cl_values)

    plt.xlim(0, 40)
    plt.ylim(0, 2.0)
    plt.xlabel('alpha, deg')
    plt.ylabel('CL')
    plt.axhline(color='grey')
    plt.savefig('figures/cl_alpha.png')
    plt.show()

plot()

#print(breakpoints['Cm'].keys())





