import scipy.io as io
import numpy as np
from scipy.interpolate import interpn


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



def aero_mat_data_parser(aero_coefficient_label, value_array):
    global aero_coefficient_names, subcoefficient_labels

    data = dict.fromkeys(subcoefficient_labels[aero_coefficient_label])
    data_idx = aero_coefficient_names.index(aero_coefficient_label)

    for idx, key in enumerate(data.keys()):

        data[key] = {}
        for var_idx, variable_name in enumerate(value_array[data_idx].item()[idx].dtype.names):
            data[key][variable_name] = value_array[data_idx].item()[idx][0][0][var_idx][0]

    return data


cx = aero_mat_data_parser('CX', discrete_points)
print(type(cx['CX']['dHT']))


temp = discrete_values[0][0][0][0]

CX_lt = interpn((cx['CX']['alpha'], cx['CX']['beta'], cx['CX']['dHT']), discrete_values[0][0][0][0])
CX_lt

#
# CX_data = dict.fromkeys(subcoefficient_labels['CX'])
#
# for idx, key in enumerate(CX_data.keys()):
#     CX_data[key] = {}
#     for var_idx, variable_name in enumerate(discrete_points[0].item()[idx].dtype.names):
#         CX_data[key][variable_name] = discrete_points[0].item()[idx][0][0][var_idx]






