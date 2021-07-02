import scipy.io as io
import numpy as np
from scipy.interpolate import interpn
import pickle

#Load the .mat data and lose the redundant nesting.
data = io.loadmat('data/f16_AerodynamicDatav7.mat')
data = data['f16_AerodynamicData']
data = data.item()

discrete_points = data[0].item()
discrete_values = data[1].item()

aero_coefficient_names = data[0].dtype.names
aero_coefficient_names = [name for name in aero_coefficient_names]

#Initialize an empty list.
subcoefficient_labels = dict.fromkeys(aero_coefficient_names)

for array, coefficient_name in zip(discrete_values, aero_coefficient_names):
    subcoefficient_labels[coefficient_name] = [subcoefficient_name for subcoefficient_name in array.dtype.names]


def aero_breakpoint_parser(aero_coefficient_name, value_array):
    global aero_coefficient_names, subcoefficient_labels

    bp_data = dict.fromkeys(subcoefficient_labels[aero_coefficient_name])
    bp_data_idx = aero_coefficient_names.index(aero_coefficient_name)

    for idx, key in enumerate(bp_data.keys()):

        bp_data[key] = {}
        for var_idx, variable_name in enumerate(value_array[bp_data_idx].item()[idx].dtype.names):
            bp_data[key][variable_name] = value_array[bp_data_idx].item()[idx][0][0][var_idx][0]

    return bp_data


def aero_value_parser(aero_coefficient_name, value_array):
    global aero_coefficient_names, subcoefficient_labels

    aero_data = dict.fromkeys(subcoefficient_labels[aero_coefficient_name])
    aero_data_idx = aero_coefficient_names.index(aero_coefficient_name)

    for idx, key in enumerate(aero_data.keys()):
        aero_data[key] = value_array[aero_data_idx].item()[idx]

    return aero_data


coefficient_breakpoints = dict.fromkeys(aero_coefficient_names)

for key in coefficient_breakpoints.keys():
    coefficient_breakpoints[key] = aero_breakpoint_parser(key, discrete_points)


coefficient_values = dict.fromkeys(aero_coefficient_names)
for key in coefficient_values.keys():
    coefficient_values[key] = aero_value_parser(key, discrete_values)


with open('data/ParsedAeroDataBPs.pkl', 'wb') as f:
    pickle.dump(coefficient_breakpoints, f)

with open('data/ParsedAeroDataValues.pkl', 'wb') as f:
    pickle.dump(coefficient_values, f)
