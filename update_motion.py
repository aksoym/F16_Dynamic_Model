import numpy as np
from gravity_model import gravity
from aero_model import get_aero_forces
from dynamic_constants import INERTIAL_MOMENTS
from numpy import cos, sin

mass = 10000

#[Vt, beta, alpha, p, q, r, x, y, z, phi, theta, psi]
state = {"Vt":0, "beta":0, "alpha":0, "p":0, "q":0, "r":0, "x":0, "y":0, "z":0, "phi":0,
    "theta":0, "psi":0}


def update_motion(plane_matrix, plane_speed_vector, dynamic_state):

    global mass, density

    #Update the states based on info from the aircraft.
    state['Vt'] = np.linalg.norm(plane_speed_vector)
    state['x'] = plane_matrix[9]
    state['y'] = plane_matrix[10]
    state['z'] = plane_matrix[11]

    #Compute the forces based on updated state variables.

    Fgravity = gravity(state['phi'], state['theta'], mass)
    Faero = get_aero_forces(density, state['Vt'], state['alpha'], state['beta'],
                            state['p'], state['q'], state['r'], deltaE, deltaA, deltaR)

    #Wind frame velocity to body frame.
    u = state['Vt'] * cos(state['alpha']) * cos(state['beta'])
    v = state['Vt'] * sin(state['beta'])
    w = state['Vt'] * sin(state['alpha']) * cos(state['beta'])

    # Translational Dynamics in Body Frame
    udot = (Fa[0] + Fp[0] + Fg[0]) / m - state['q'] * w + state['r'] * v
    vdot = (Fa[1] + Fp[1] + Fg[1]) / m - state['r'] * u + state['p'] * w
    wdot = (Fa[2] + Fp[2] + Fg[2]) / m - state['p'] * v + state['q'] * u

    # Transformation acceleration body - to - wind axis

    invewb = np.array([
        [cos(state['alpha']) * cos(state['beta']), sin(state['beta'])      sin(state['alpha']) * cos(state['beta'])],
        [- cos(state['alpha']) * sin(state['beta']) / state['Vt'], cos(state['beta']) / state['Vt'],  -sin(state['alpha']) * sin(state['beta']) / state['Vt']],
        [- sin(state['alpha']) / (state['Vt'] * cos(state['beta'])), 0, cos(state['alpha']) / (state['Vt'] * cos(state['beta']))]
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
        [0, -state['r'], state['q']],
        [state['r'], 0, -state['p']],
        [-state['q'], state['p'], 0]
    ])

    #Rotational Dynamics
    rot_dot = np.linalg.inv(INERTIAL_MOMENTS) * (moments - pqr * Inertia * [state['p'];state['q'];state['r']]);
    pdot = rot_dot[0]
    qdot = rot_dot[1]
    rdot = rot_dot[2]

    # Translational Kinematics Equations Rotation in x - axis with phi euler angle
    rotx = np.array([
        [1, 0, 0],
        [0, cos(state['phi']), sin(state['phi'])],
        [0, -sin(state['phi']), cos(state['phi'])]
    ])


    # Rotation in y - axis with theta euler angle
    roty = np.array([
        [cos(state['theta']), 0, -sin(state['theta'])],
        [0, 1, 0],
        [sin(state['theta']), 0, cos(state['theta'])]
    ])



    # Rotation in z - axis with psi euler angle
    rotz = np.array([
        [cos(state['psi']), sin(state['psi']), 0],
        [-sin(state['psi']), cos(state['psi']), 0],
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


    x = numpy.array([Vtdot, betadot, alphadot, pdot, qdot, rdot, xdot, ydot, zdot,
                     phidot, thetadot, psidot])

    return x
