import numpy as np
from numpy import typename

zero_epsilon = 10e-3


#TRIGINOMETRIC FUNCTIONS. Altered to work with angles instead of radians.
def cos(x):
    return np.cos(np.deg2rad(x))


def sin(x):
    return np.sin(np.deg2rad(x))


def tan(x):
    return np.tan(np.deg2rad(x))


def cotan(x):
    return 1 / tan(x)


def sec(x):
    return 1 / cos(x)


def cosec(x):
    return 1 / sin(x)


def arctan(x):
    return np.rad2deg(np.arctan(x))


def arcsin(x):
    return np.rad2deg(np.arcsin(x))

def arccos(x):
    return np.rad2deg(np.arccos(x))



#Theta and phi finder.
def get_theta_and_phi_from_rotation_matrix(matrix):
    """

    :param matrix: ndarray
    :return: theta and beta in degrees as a tuple.
    """

    assert isinstance(matrix, np.ndarray), "The input must be a numpy array."
    assert matrix.shape == (3, 3), "The matrix must have dimensions (3, 3)"

    phi = arccos(matrix[1][1])
    theta = arctan(matrix[0][1] / sin(phi)) if sin(phi) > zero_epsilon else 0.0

    assert abs(phi) < 60, f"Roll limit is reached. {phi}"
    assert abs(theta) < 45, f"AoA limit is reached, flight model is NOT configured to provide accurate dynamics in this AoA range. {theta}"

    return (theta, phi)
