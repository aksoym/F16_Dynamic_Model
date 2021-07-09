import pickle
from  scipy.interpolate import interpn
import numpy as np
from math_tools import sin, cos

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


def _coefficient(label, point):
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

        coef_list.append(interpn(tuple(bp.values()), flat_out(value), np.array([point[i] for i in idx_for_needed_params]), bounds_error=False, fill_value=None))

    coef_list = [scalar_array.item() for scalar_array in coef_list]
    return tuple(coef_list)


def get_aero_force_coefficients(velocity, alpha, beta, p, q, r, deltaE, deltaA, deltaR, deltaLEF, deltaSB):
    global WING_SPAN, WING_AREA, CHORD_LENGTH

    interp_coord = (alpha, beta, deltaE)

    coefs = _coefficient('CX', interp_coord)
    deltaCoefs = _coefficient('CX', (alpha, beta, 0))
    calculate_CX = coefs[0] \
                   + (coefs[1] - deltaCoefs[0]) * (1 - deltaLEF/25) \
                   + coefs[4] * (deltaSB/60) \
                   + ((CHORD_LENGTH * q) / 2*velocity) * (coefs[2] + coefs[3]*(1 - deltaLEF/25))

    coefs = _coefficient('CZ', interp_coord)
    deltaCoefs = _coefficient('CZ', (alpha, beta, 0))
    calculate_CZ = coefs[0] \
                   + (coefs[1] - deltaCoefs[0]) * (1 - deltaLEF/25) \
                   + coefs[4] * (deltaSB/60) \
                   + ((CHORD_LENGTH*q) / 2*velocity) * (coefs[2] + coefs[3] * (1 - deltaLEF/25))

    coefs = _coefficient('CY', interp_coord)
    calculate_CY = coefs[0] \
                   + (coefs[1] - coefs[0]) * (1 - deltaLEF/25) \
                   + ((coefs[2] - coefs[0]) + (coefs[3] - coefs[1] - coefs[2] + coefs[0]) * (1 - deltaLEF/25)) * (deltaA/20) \
                   + (coefs[4] - coefs[0]) * (deltaR/30) \
                   + (WING_SPAN / 2*velocity) * ((coefs[5] + coefs[6] * (1 - deltaLEF/25)) * r
                                                 + (coefs[7] + coefs[8] * (1 - deltaLEF/25))*p)

    lift_coef = -calculate_CZ * cos(alpha) + calculate_CX * sin(alpha)
    drag_coef = -calculate_CZ * sin(alpha) - calculate_CX * cos(alpha)

    return (calculate_CX, calculate_CY, calculate_CZ, lift_coef, drag_coef)


def get_aero_forces(density, velocity, alpha, beta, p, q, r, deltaE, deltaA, deltaR, deltaLEF, deltaSB):
    global WING_AREA
    coefs = get_aero_force_coefficients(velocity, alpha, beta, p, q, r, deltaE, deltaA, deltaR, deltaLEF, deltaSB)
    coefs = np.array(coefs[:3])

    force_term = (density * (velocity**2) / 2) * WING_AREA

    return tuple(coefs * force_term)



def get_aero_moment_coefficients(velocity, alpha, beta, p, q, r, deltaE, deltaA, deltaR, deltaLEF, deltaSB):
    global WING_SPAN, WING_AREA, CHORD_LENGTH

    interp_coord = (alpha, beta, deltaE)

    coefs = _coefficient('Cm', interp_coord)
    deltaCoefs = _coefficient('Cm', (alpha, beta, 0))
    calculate_Cm = coefs[0] * coefs[6] \
                   + (coefs[1] - deltaCoefs[0]) * (1 - deltaLEF/25) \
                   + coefs[7] * (deltaSB/60) \
                   + (CHORD_LENGTH * q) / (2*velocity) * (coefs[2] + coefs[3] * (1 - deltaLEF/25)) \
                   + coefs[4] \
                   + coefs[5]


    coefs = _coefficient('Cn', interp_coord)
    deltaCoefs = _coefficient('Cn', (alpha, beta, 0))
    calculate_Cn = coefs[0] \
                   + (coefs[1] - deltaCoefs[0]) * (1 - deltaLEF/25) \
                   + ((coefs[2] - deltaCoefs[0]) + (coefs[3] - coefs[1] - coefs[2] + deltaCoefs[0]) * (1 - deltaLEF/25)) * (deltaA/20) \
                   + (coefs[4] - deltaCoefs[0]) * (deltaR/30) \
                   + WING_SPAN / (2*velocity) * ((coefs[5] + coefs[6] * (1 - deltaLEF/25)) * r
                                                 + (coefs[7] + coefs[8] * (1 - deltaLEF/25)) * p) \
                   + coefs[9]

    coefs = _coefficient('Cl', interp_coord)
    deltaCoefs = _coefficient('Cl', (alpha, beta, 0))
    calculate_Cl = coefs[0] \
                   + (coefs[1] - deltaCoefs[0]) * (1 - deltaLEF/25) \
                   + ((coefs[2] - deltaCoefs[0]) + (coefs[3] - coefs[1] - coefs[2] + deltaCoefs[0]) * (1 - deltaLEF/25)) * (deltaA/20) \
                   + (coefs[4] - deltaCoefs[0]) * (deltaR/30) \
                   + WING_SPAN / (2*velocity) * ((coefs[5] + coefs[6] * (1 - deltaLEF/25)) * r
                                                 + (coefs[7] + coefs[8] * (1 - deltaLEF/25)) * p) \
                   + coefs[9]

    return (calculate_Cl, calculate_Cm, calculate_Cn)




def get_aero_moments(density, velocity, alpha, beta, p, q, r, deltaE, deltaA, deltaR, deltaLEF, deltaSB):
    global WING_SPAN, CHORD_LENGTH, WING_AREA
    coefs = get_aero_moment_coefficients(velocity, alpha, beta, p, q, r, deltaE, deltaA, deltaR, deltaLEF, deltaSB)
    coefs = np.array(coefs)

    dynamic_pressure = density * (velocity**2) / 2
    dynamic_force = dynamic_pressure * WING_AREA
    multiply_terms = np.array([dynamic_force * WING_SPAN, dynamic_force * CHORD_LENGTH, dynamic_force * WING_SPAN])

    return tuple(np.multiply(coefs, multiply_terms))