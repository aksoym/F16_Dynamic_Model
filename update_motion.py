import numpy as np
from gravity_model import gravity
from aero_model import get_aero_forces, get_aero_moments
from dynamic_tools import INERTIAL_MOMENTS
from propulsion_model import propulsion
from gyro_model import gyroscopic
from math_tools import cos, sin, get_theta_and_phi_from_rotation_matrix

mass = 9298.6

#[Vt, beta, alpha, p, q, r, x, y, z, phi, theta, psi]
state = {"Vt":100, "beta":0, "alpha":4, "p":0, "q":0, "r":0, "x":0, "y":0, "z":10000, "phi":0,
    "theta":2, "psi":0}


def update_motion(plane_matrix, plane_speed_vector,
                  state, deltaE, deltaA, deltaR, thrust_lever):

    global mass


    #Get atmospheric properties. state 'z' is referenced as the altitude.
    #density, speed_of_sound = atmosphere(state['z'])

    #Update the states based on info from the aircraft.
    state['Vt'] = np.linalg.norm(plane_speed_vector)

    kinematic_rotation_matrix = plane_matrix[:9].reshape(3, 3)

    state['theta'], state['beta'] = get_theta_and_phi_from_rotation_matrix(kinematic_rotation_matrix)

    state['x'] = plane_matrix[9]
    state['y'] = plane_matrix[10]
    state['z'] = plane_matrix[11]

    altitude = state['z']

    density = 1.225 * 0.3376
    speed_of_sound = 295

    mach = state['Vt'] / speed_of_sound

    #Compute the forces based on updated state variables.

    Fgravity = gravity(state['phi'], state['theta'], mass)
    Faero = get_aero_forces(density, state['Vt'], state['alpha'], state['beta'],
                            state['p'], state['q'], state['r'], deltaE, deltaA, deltaR)
    Fprop = propulsion(thrust_lever, mach, altitude)[0]


    #Compute moments around body axis.
    Mgyro = gyroscopic(state['p'], state['q'], state['r'])
    Maero = get_aero_moments(density, state['Vt'], state['alpha'], state['beta'],
                            state['p'], state['q'], state['r'], deltaE, deltaA, deltaR)

    Mprop = propulsion(thrust_lever, mach, altitude)[1]

    #Wind frame velocity to body frame.
    u = state['Vt'] * cos(state['alpha']) * cos(state['beta'])
    v = state['Vt'] * sin(state['beta'])
    w = state['Vt'] * sin(state['alpha']) * cos(state['beta'])

    # Translational Dynamics in Body Frame
    udot = (Faero[0] + Fprop[0] + Fgravity[0]) / mass - state['q'] * w + state['r'] * v
    vdot = (Faero[1] + Fprop[1] + Fgravity[1]) / mass - state['r'] * u + state['p'] * w
    wdot = (Faero[2] + Fprop[2] + Fgravity[2]) / mass - state['p'] * v + state['q'] * u

    # Transformation acceleration body - to - wind axis

    invewb = np.array([
        [cos(state['alpha']) * cos(state['beta']), sin(state['beta']), sin(state['alpha']) * cos(state['beta'])],
        [- cos(state['alpha']) * sin(state['beta']) / state['Vt'], cos(state['beta']) / state['Vt'],  -sin(state['alpha']) * sin(state['beta']) / state['Vt']],
        [- sin(state['alpha']) / (state['Vt'] * cos(state['beta'])), 0, cos(state['alpha']) / (state['Vt'] * cos(state['beta']))]
    ])

    #Translational dynamics in the wind frame.

    translational_dynamics = np.matmul(invewb, np.array([udot, vdot, wdot]))
    Vtdot = translational_dynamics[0]
    betadot = translational_dynamics[1]
    alphadot = translational_dynamics[2]

    # Rotational Dynamics in Body Frame
    moments = np.array([
        [Maero[0] + Mprop[0] + Mgyro[0]],
        [Maero[1] + Mprop[1] + Mgyro[1]],
        [Maero[2] + Mprop[2] + Mgyro[2]]
    ]).reshape(3, 1)

    pqr = np.array([
        [0, -state['r'], state['q']],
        [state['r'], 0, -state['p']],
        [-state['q'], state['p'], 0]
    ])

    #Rotational Dynamics
    rot_dot = np.matmul(np.linalg.inv(INERTIAL_MOMENTS), (moments - np.matmul(np.matmul(pqr, INERTIAL_MOMENTS), np.array([[state['p']],
                                                                                                                          [state['q']],
                                                                                                                          [state['r']]]))))
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
    translational_kinematics = np.matmul(body_to_earth_frame, np.array([[u],
                                                                        [v],
                                                                        [w]]))
    xdot = translational_kinematics[0]
    ydot = translational_kinematics[1]
    zdot = translational_kinematics[2]

    #Rotational kinematics.

    # kinematic_rotation_matrix = np.array([
    #     [1, tan(state['theta'])*sin(state['phi']), cos(state['phi'])*tan(state['theta'])],
    #     [0, cos(state['phi']), -sin(state['phi'])],
    #     [0, sec(state['theta'])*sin(state['phi']), sec(state['theta'])*cos(state['phi'])]
    # ])


    rotational_kinematics = np.matmul(kinematic_rotation_matrix, np.array([[state['p']],
                                                                           [state['q']],
                                                                           [state['r']]]))
    phidot = rotational_kinematics[0]
    thetadot = rotational_kinematics[1]
    psidot = rotational_kinematics[2]


    dotstate_variables = [Vtdot, betadot, alphadot, pdot, qdot, rdot, xdot, ydot, zdot, phidot, thetadot, psidot]
    state_diff = np.array([variable.item() for variable in dotstate_variables])

    updated_state = dict()

    for variable_index, key in enumerate(state.keys()):
        updated_state[key] = state[key] + state_diff[variable_index]

    resulting_plane_matrix = np.array([
        1, tan(state['theta'])*sin(state['phi']), cos(state['phi'])*tan(state['theta']),
        0, cos(state['phi']), -sin(state['phi']),
        0, sec(state['theta'])*sin(state['phi']), sec(state['theta'])*cos(state['phi']),
        state['x'], state['y'], state['z']
    ])

    resulting_plane_speed_vector = np.array([
        u, v, w
    ])


    return resulting_plane_matrix, resulting_plane_speed_vector, updated_state, state_diff



#UPDATE MOTION UNIT TEST.
