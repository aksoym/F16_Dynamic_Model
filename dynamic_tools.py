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

#Stability derivatives polynomial coefficeints.
coefficient_dict = {}
coefficient_dict['a'] = (-1.943367e-02, 2.136104e-01, -2.903457e-01, -3.348641e-03, -2.060504e-01, 6.988016e-01, -9.035381e-01)
coefficient_dict['b'] = (4.833383e-01, 8.644627e+00, 1.131098e+01, -7.422961e+01, 6.075776e+01)
coefficient_dict['c'] = (-1.145916e+00, 6.016057e-02, 1.642479e-01)
coefficient_dict['d'] = (-1.006733e-01, 8.679799e-01, 4.260586e+00, -6.923267e+00)
coefficient_dict['e'] = (8.071648e-01, 1.189633e-01, 4.177702e+00, -9.162236e+00)
coefficient_dict['f'] = (-1.378278e-01, -4.211369e+00, 4.775187e+00, -1.026225e+01, 8.399763e+00, -4.354000e-01)
coefficient_dict['g'] = (3.054956e+01, -4.132305e+01, -4.132305e+01, -6.848038e+02, 4.080244e+02)
coefficient_dict['h'] = (-1.058583e-01, -5.776677e-01, -1.672435e-02, 1.357256e-01, 2.172952e-01, 3.464156e+00, -2.835451e+00, -1.098104e+00)
coefficient_dict['i'] = (-4.126806e-01, -1.189974e-01, 1.247721e+00, -7.391132e-01)
coefficient_dict['j'] = (6.250437e-02, 6.067723e-01, -1.101964e+00, 9.100087e+00, -1.192672e+01)
coefficient_dict['k'] = (-1.463144e-01, -4.073901e-02, 3.253159e-02, 4.851209e-01, 2.978850e-01, -3.746393e-01, -3.213068e-01)
coefficient_dict['l'] = (2.635729e-02, -2.192910e-02, -3.152901e-03, -5.817803e-02, 4.516159e-01, -4.928702e-01, -1.579864e-02)
coefficient_dict['m'] = (-2.029370e-02, 4.660702e-02, -6.012308e-01, -8.062977e-02, 8.320429e-02, 5.018538e-01, 6.378864e-01, 4.226356e-01)
coefficient_dict['n'] = (-5.159153e+00, -3.554716e+00, -3.598636e+01, 2.247355e+02, -4.120991e+02, 2.411750e+02)
coefficient_dict['o'] = (2.993363e-01, 6.594004e-02, -2.003125e-01, -6.233977e-02, -2.107885e+00, 2.141420e+00, 8.476901e-01)
coefficient_dict['p'] = (2.677652e-02, -3.298246e-01, 1.926178e-01, 4.013325e+00, -4.404302e+00)
coefficient_dict['q'] = (-3.698756e-01, -1.167551e-01, -7.641297e-01)
coefficient_dict['r'] = (-3.348717e-02, 4.276655e-02, 6.573646e-03, 3.535831e-01, -1.373308e+00, 1.237582e+00, 2.302543e-01, -2.512876e-01, 1.588105e-01, -5.199526e-01)
coefficient_dict['s'] = (-8.115894e-02, -1.156580e-02, 2.514167e-02, 2.038748e-01, -3.337476e-01, 1.004297e-0)


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
