import matplotlib.pyplot as plt
import numpy as np
from typing import Callable, Optional, Tuple, Dict
from aero_model import derivatives


class Monitor():

    def __init__(self,
                 function: Callable[[float, float, float, float, float], dict],
                 arguments_high: Tuple[float, ...] = (45, 30, 25, 21.5, 30),
                 arguments_low: Tuple[float, ...] = (-10, -30, -25, -21.5, -30)):

        self.function = function
        self.arguments_high = arguments_high
        self.arguments_low = arguments_low
        self.default_arg_vals = {'alpha':0, 'beta':0, 'deltaE':0, 'deltaA':0, 'deltaR':0}


    def plot(self,
             argument_key: str,
             variable_key: str,
             variable_resolution: Optional[int] = 50):

        figure = plt.figure(figsize=(10, 10))

        argument_index = {'alpha':0, 'beta':1, 'deltaE':2, 'deltaA':3, 'deltaR':4}
        x = np.linspace(self.arguments_low[argument_index[argument_key]],
                        self.arguments_high[argument_index[argument_key]],
                        variable_resolution)



        y = []
        for x_var in x:
            argument_template = list(self.default_arg_vals.values())
            argument_template[argument_index[argument_key]] = x_var
            argument_template = tuple(argument_template)

            y.append(self.function(*argument_template).get(variable_key))

        plt.plot(x, y)
        plt.xlabel(f'{argument_key}')
        plt.ylabel(f'{variable_key}')
        plt.show()






monitor = Monitor(derivatives)

monitor.plot('alpha', 'CL')








