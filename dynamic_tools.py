import numpy as np
from math_tools import cos, sin, tan, arctan, sec, cosec, arcsin, arccos

#Gyroscopic and propulsion moment constants.
ANGULAR_MOMENTUM = np.array([[216.9],
                            [0],
                            [0]])

theta_eng = 0 #in radians.
psi_eng = 0 #in radians.
ENGINE_ORIENTATION = (theta_eng, psi_eng)
ENGINE_OFFSET = np.array([
    [0],
    [0],
    [0]
])


#equations of motion

Ixx = 12875
Ixy = 0
Iyy = 75674
Izz = 85552
Ixz = 1331
Iyz = 0

INERTIAL_MOMENTS = np.array([[Ixx, -Ixy, -Ixz],
                            [-Ixy, Iyy, -Iyz],
                            [-Ixz, -Iyz, Izz]])
