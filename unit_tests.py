from update_motion import update_motion
import timeit
import numpy as np







def update_motion_unit_test(function):

    #Arguments.

    state = {"Vt": 100, "beta": 0, "alpha": 4, "p": 0, "q": 0, "r": 0, "x": 0, "y": 0, "z": 10000, "phi": 0,
             "theta": 2, "psi": 0}

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

    thrust_lever = 0.5

    result = function(plane_matrix, plane_speed_vector, state, deltaE, deltaA, deltaR, thrust_lever)


    print(result)
    print(timeit.default_timer(function(plane_matrix, plane_speed_vector, state, deltaE, deltaA, deltaR, thrust_lever)))


update_motion_unit_test(update_motion)
