import numpy as np

GRAVITY = 9.81

def gravity(phi, theta, mass):
    """
    Computes the gravity forces acting on the aircraft body. Returns the force vector
    tuple in body frame.

    :param g: gravital acceleration in meter per square seconds
    :param phi:
    :param theta:
    :param mass:
    :return:
    """
    theta = theta * np.pi / 180
    phi = phi * np.pi / 180
    Fx = -mass * GRAVITY * np.sin(theta)
    Fy = mass * GRAVITY * np.cos(theta) * np.sin(phi)
    Fz = mass * GRAVITY * np.cos(theta) * np.cos(phi)

    return (Fx, Fy, Fz)