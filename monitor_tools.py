import matplotlib.pyplot as plt
import numpy as np
from typing import Callable, Optional, Tuple


class Monitor():

    def __init__(self,
                 function = Callable[[float, float, float, float, float], dict],
                 arguments_high: Tuple[float, ...] = (45, 30, 25, 21.5, 30),
                 arguments_low: Tuple[float, ...] = (-10, -30, -25, -21.5, -30))

        self.function = function
        self.arguments_high = arguments_high
        self.arguments_low = arguments_low


    def plot(self,
             variables: List[int],
             plot_dim: Optional[int] = 2,
             static_variable: Optional[int] = None,
             **kwargs)

        figure = plt.figure(figsize=())

