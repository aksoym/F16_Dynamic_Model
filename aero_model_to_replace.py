import pickle
from  scipy.interpolate import interpn
import numpy as np

CHORD_LENGTH = 3.45
WING_AREA = 27.87
WING_SPAN = 9.144

with open('data/ParsedAeroDataBPs.pkl', 'rb') as f:
    breakpoints = pickle.load(f)

with open('data/ParsedAeroDataValues.pkl', 'rb') as f:
    values = pickle.load(f)

parameter_names = ('alpha', 'beta', 'dHT')

def flat_out(array):
    if array.shape[0] == 1 and array.shape[1]:
        return array.flatten()
    else:
        return array


def coefficient(label, point):
    global breakpoints, values, parameter_names
    bp_data = breakpoints[label]
    value_data = values[label]

    coef_list = []
    for bp, value in zip(bp_data.values(), value_data.values()):

        idx_for_needed_params = []
        for key_name in bp.keys():
            for i, name in enumerate(parameter_names):
                if key_name == name:
                    idx_for_needed_params.append(i)

        coef_list.append(interpn(tuple(bp.values()), flat_out(value), np.array([point[i] for i in idx_for_needed_params])))

    coef_list = [scalar_array.item() for scalar_array in coef_list]
    return tuple(coef_list)


def get_aero_force_coefficients(velocity, alpha, beta, p, q, r, deltaE, deltaA, deltaR, deltaLEF, deltaSB):
    global WING_SPAN, WING_AREA, CHORD_LENGTH

    interp_coord = (alpha, beta, deltaE)

    coefs = coefficient('CX', interp_coord)
    deltaCoefs = coefficient('CX', (alpha, beta, 0))
    calculate_CX = coefs[0] \
                   + (coefs[1] - deltaCoefs[0]) * (1 - deltaLEF/25) \
                   + coefs[4] * (deltaSB/60) \
                   + ((CHORD_LENGTH * q) / 2*velocity) * (coefs[2] + coefs[3]*(1 - deltaLEF/25))

    coefs = coefficient('CZ', interp_coord)
    deltaCoefs = coefficient('CZ', (alpha, beta, 0))
    calculate_CZ = coefs[0] \
                   + (coefs[1] - deltaCoefs[0]) * (1 - deltaLEF/25) \
                   + coefs[4] * (deltaSB/60) \
                   + ((CHORD_LENGTH*q) / 2*velocity) * (coefs[2] + coefs[3] * (1 - deltaLEF/25))

    coefs = coefficient('CY', interp_coord)
    calculate_CY = coefs[0] \
                   + (coefs[1] - coefs[0]) * (1 - deltaLEF/25) \
                   + ((coefs[2] - coefs[0]) + (coefs[3] - coefs[1] - coefs[2] + coefs[0]) * (1 - deltaLEF/25)) * (deltaA/20) \
                   + (coefs[4] - coefs[0]) * (deltaR/30) \
                   + (WING_SPAN / 2*velocity) * ((coefs[5] + coefs[6] * (1 - deltaLEF/25)) * r
                                                 + (coefs[7] + coefs[8] * (1 - deltaLEF/25))*p)

    return (calculate_CX, calculate_CY, calculate_CZ)


def get_aero_forces(density, velocity, alpha, beta, p, q, r, deltaE, deltaA, deltaR, deltaLEF, deltaSB):
    global WING_AREA
    coefs = get_aero_force_coefficients(velocity, alpha, beta, p, q, r, deltaE, deltaA, deltaR, deltaLEF, deltaSB)
    coefs = np.array(coefs)

    force_term = (density * (velocity**2) / 2) * WING_AREA

    return tuple(coefs * force_term)
