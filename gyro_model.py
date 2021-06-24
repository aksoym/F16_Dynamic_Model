import numpy as np
from dynamic_tools import ANGULAR_MOMENTUM, ENGINE_ORIENTATION
from math_tools import cos, sin, tan, arctan, sec, cosec, arcsin, arccos


def gyroscopic(p, q, r):
    """
    Computes the gyroscopic moment acting on the aircraft.

    :param p: angular rate around x axis.
    :param q: angular rate around y axis.
    :param r: angular rate around z axis.
    :return: gyroscopic moment, a scalar.
    """

    angular_speed_mat = np.array([[p],
                                  [q],
                                  [r]])

    y_rot_mat = np.array([
        [cos(ENGINE_ORIENTATION[0]), 0, -sin(ENGINE_ORIENTATION[0])],
        [0, 1, 0],
        [sin(ENGINE_ORIENTATION[0]), 0, cos(ENGINE_ORIENTATION[0])]
    ])

    z_rot_mat = np.array([
        [cos(ENGINE_ORIENTATION[1]), sin(ENGINE_ORIENTATION[1]), 0],
        [sin(ENGINE_ORIENTATION[1]), cos(ENGINE_ORIENTATION[1]), 0],
        [0, 0, 1]
    ])

    body_to_prop_tm = np.matmul(y_rot_mat, z_rot_mat)
    prop_to_body_tm = np.linalg.inv(body_to_prop_tm)

    acting_angular_momentum = np.matmul(prop_to_body_tm, ANGULAR_MOMENTUM)


    resulting_gyroscopic_moment = -np.cross(angular_speed_mat, acting_angular_momentum, axisa=0, axisb=0).reshape(-1, 1)

    return resulting_gyroscopic_moment

