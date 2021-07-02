import pickle
from  scipy.interpolate import interpn
import numpy as np

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


val = interpn(tuple(breakpoints['CZ']['CZ'].values()), values['CZ']['CZ'], (10, 0, 0))
print(val)

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

        print(bp.values(), flat_out(value), idx_for_needed_params, sep='\n')
        coef_list.append(interpn(tuple(bp.values()), flat_out(value), np.array([point[i] for i in idx_for_needed_params])))

    coef_list = [scalar_array.item() for scalar_array in coef_list]
    return tuple(coef_list)


print(coefficient('Cm', (4, 0, -5)))


def get_aero_forces(density, velocity, alpha, beta, p, q, r, deltaE, deltaA, deltaR):
    interp_coord = (alpha, beta, deltaE)

    coefs = coefficient('CX', interp_coord)
    calculate_CX = coefs[0] +