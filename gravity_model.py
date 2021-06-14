import numpy as np

def gravity(g, phi, theta, mass):
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
    Fx = -mass * g * np.sin(theta)
    Fy = mass * g * np.cos(theta) * np.sin(phi)
    Fz = mass * g * np.cos(theta) * np.cos(phi)

    return (Fx, Fy, Fz)