import numpy as np


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
