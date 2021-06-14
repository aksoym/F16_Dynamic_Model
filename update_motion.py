import numpy as np
from dynamic_constants import INERTIAL_MOMENTS
from numpy import cos, sin


def update_motion(Fa, Ma, Fg, Mgy, p, q, r, phi, theta, psi, alpha, beta, Vt, m):


    #Wind frame velocity to body frame.
    u = Vt * cos(alpha) * cos(beta)
    v = Vt * sin(beta)
    w = Vt * sin(alpha) * cos(beta)

    # Translational Dynamics in Body Frame
    udot = (Fa[0] + Fp[0] + Fg[0]) / m - q * w + r * v
    vdot = (Fa[1] + Fp[1] + Fg[1]) / m - r * u + p * w
    wdot = (Fa[2] + Fp[2] + Fg[2]) / m - p * v + q * u

    # Transformation acceleration body - to - wind axis

    invewb = np.array([
        [cos(alpha) * cos(beta), sin(beta)      sin(alpha) * cos(beta)],
        [- cos(alpha) * sin(beta) / Vt, cos(beta) / Vt,  -sin(alpha) * sin(beta) / Vt],
        [- sin(alpha) / (Vt * cos(beta)), 0, cos(alpha) / (Vt * cos(beta))]
    ])

    #Translational dynamics in the wind frame.

    translational_dynamics = invewb * np.array([[udot], [vdot], [wdot]])
    Vtdot = translational_dynamics[0]
    betadot = translational_dynamics[1]
    alphadot = translational_dynamics[2]

    # Rotational Dynamics in Body Frame
    moments = np.array([
        [Ma[0] + Mp[0] + Mgy[0]],
        [Ma[1] + Mp[1] + Mgy[1]],
        [Ma[2] + Mp[2] + Mgy[2]]
    ])

    pqr = np.array([
        [0, -r, q],
        [r, 0, -p],
        [-q, p, 0]
    ])

    #Rotational Dynamics
    rot_dot = np.linalg.inv(INERTIAL_MOMENTS) * (moments - pqr * Inertia * [p;q;r]);
    pdot = rot_dot[0]
    qdot = rot_dot[1]
    rdot = rot_dot[2]

    # Translational Kinematics Equations Rotation in x - axis with phi euler angle
    rotx = np.array([
        [1, 0, 0],
        [0, cos(phi), sin(phi)],
        [0, -sin(phi), cos(phi)]
    ])


    # Rotation in y - axis with theta euler angle
    roty = np.array([
        [cos(theta), 0, -sin(theta)],
        [0, 1, 0],
        [sin(theta), 0, cos(theta)]
    ])



    # Rotation in z - axis with psi euler angle
    rotz = np.array([
        [cos(psi), sin(psi), 0],
        [-sin(psi), cos(psi), 0],
        [0, 0, 1]
    ])

    # Transformation Earth - to - Body Frame
    earth_to_body_frame = np.matmul(np.matmul(rotx, roty), rotz)


    #Transformation Body - to - Earth Frame
    body_to_earth_frame = np.linalg.inv(earth_to_body_frame)


    # Translational Kinematics in Earth Frame
    translational_kinematics = np.matmul(body_to_earth_frame, np.array([u, v, w]))
    xdot = translational_kinematics[0]
    ydot = translational_kinematics[1]
    zdot = translational_kinematics[2]


    x = [Vtdot, betadot, alphadot, pdot, qdot, rdot, xdot, ydot, zdot, phidot, thetadot, psidot]

    return x
