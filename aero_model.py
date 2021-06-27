import numpy as np
from dynamic_tools import coefficient_dict
from math_tools import cos, sin, tan, arctan, sec, cosec, arcsin, arccos

CHORD_LENGTH = 3.45
WING_AREA = 27.87
WING_SPAN = 9.144


def cx(alpha, deltaE):
    a0, a1, a2, a3, a4, a5, a6 = coefficient_dict['a']
    return a0 + a1*alpha + a2*(deltaE**2) + a3*deltaE + a4*alpha*deltaE + a5*(alpha**2) + a6*(alpha**3)

def cxQ(alpha):
    b0, b1, b2, b3, b4 = coefficient_dict['b']
    return b0 + b1*alpha + b2*(alpha**2) + b3*(alpha**3) + b4*(alpha**4)

def cy(beta, deltaA, deltaR):
    c0, c1, c2 = coefficient_dict['c']
    return c0*beta + c1*deltaA + c2*deltaR

def cyP(alpha):
    d0, d1, d2, d3 = coefficient_dict['d']
    return d0 + d1*alpha + d2*(alpha**2) + d3*(alpha**3)

def cyR(alpha):
    e0, e1, e2, e3 = coefficient_dict['e']
    return e0 + e1*alpha + e2*(alpha**2) + e3*(alpha**3)

def cz(alpha, beta, deltaE):
    f0, f1, f2, f3, f4, f5 = coefficient_dict['f']
    return (1 - beta**2)*(f0 + f1*alpha + f2*(alpha**2) + f3*(alpha**3) + f4*(alpha**4)) + f5*deltaE

def czQ(alpha):
    g0, g1, g2, g3, g4 = coefficient_dict['g']
    return g0 + g1*alpha + g2*(alpha**2) + g3*(alpha**3) + g4*(alpha**4)

def cl(alpha, beta):
    h0, h1, h2, h3, h4, h5, h6, h7 = coefficient_dict['h']
    return h0*beta + h1*beta*alpha + h2*beta*(alpha**2) + h3*(beta**2) + h4*(beta**2)*alpha + h5*beta*(alpha**3) + h6*beta*(alpha**4) + h7*(beta**2)*(alpha**2)

def clP(alpha):
    i0, i1, i2, i3 = coefficient_dict['i']
    return i0 + i1*alpha + i2*(alpha**2) + i3*(alpha**3)

def clR(alpha):
    j0, j1, j2, j3, j4 = coefficient_dict['j']
    return j0 + j1*alpha + j2*(alpha**2) + j3*(alpha**3) + j4*(alpha**4)

def clDeltaA(alpha, beta):
    k0, k1, k2, k3, k4, k5, k6 = coefficient_dict['k']
    return k0 + k1*alpha + k2*beta + k3*(alpha**2) + k4*alpha*beta + k5*(alpha**2)*beta + k6*(alpha**3)

def clDeltaR(alpha, beta):
    l0, l1, l2, l3, l4, l5, l6 = coefficient_dict['l']
    return l0 + l1*alpha + l2*beta + l3*alpha*beta + l4*(alpha**2)*beta + l5*(alpha**3)*beta + l6*(beta**2)

def cm(alpha, deltaE):
    m0, m1, m2, m3, m4, m5, m6, m7 = coefficient_dict['m']
    return m0 + m1*alpha + m2*deltaE + m3*alpha*deltaE + m4*(deltaE**2) + m5*(alpha**2)*(deltaE) + m6*(deltaE**3) + m7*alpha*(deltaE**2)

def cmQ(alpha):
    n0, n1, n2, n3, n4, n5 = coefficient_dict['n']
    return n0 + n1*alpha + n2*(alpha**2) + n3*(alpha**3) + n4*(alpha**4) + n5*(alpha**5)

def cn(alpha, beta):
    o0, o1, o2, o3, o4, o5, o6 = coefficient_dict['o']
    return o0*beta + o1*alpha*beta + o2*(beta**2) + o3*(alpha)*(beta**2) + o4*(alpha**2)*beta + o5*(alpha**2)*(beta**2) + o6*(alpha**3)*beta

def cnP(alpha):
    p0, p1, p2, p3, p4 = coefficient_dict['p']
    return p0 + p1*alpha + p2*(alpha**2) + p3*(alpha**3) + p4*(alpha**4)

def cnR(alpha):
    q0, q1, q2 = coefficient_dict['q']
    return q0 + q1*alpha + q2*(alpha**2)

def cnDeltaA(alpha, beta):
    r0, r1, r2, r3, r4, r5, r6, r7, r8, r9 = coefficient_dict['r']
    return r0 + r1*alpha + r2*beta + r3*alpha*beta + r4*(alpha**2)*beta + r5*(alpha**3)*beta + r6*(alpha**2) + r7*(alpha**3) + r8*(beta**3) + r9*alpha*(beta**3)

def cnDeltaR(alpha, beta):
    s0, s1, s2, s3, s4, s5 = coefficient_dict['s']
    return s0 + s1*alpha + s2*beta + s3*alpha*beta + s4*(alpha**2)*beta + s5*(alpha**2)

def CL(cx, cz, alpha):
    return cz*cos(alpha) - cx*sin(alpha)

def CD(cx, cz, alpha):
    return cz*sin(alpha) + cx*cos(alpha)

def derivatives(alpha, beta, deltaE, deltaA, deltaR):
    """
    Returns the stability derivatives as a tuple. The order is as follows (you can copy this sequence for unpacking):
    (cx, cxQ, cy, cyP, cyR, cz, czQ, cl, clP, clR, clDeltaA, clDeltaR, cm, cmQ, cn, cnP, cnR, cnDeltaA, cnDeltaR).


    :param alpha: ranges in [-10, 45] degrees.
    :param beta: ranges in [-30, 30] degrees.
    :param deltaE: ranges in [-25, 25] degrees.
    :param deltaA: ranges in [-21.5, 21.5] degrees.
    :param deltaR: ranges in [-30, 30] degrees.
    :return: tuple of stability derivatives.
    """

    #Checking for boundaries.
    assert -10 <= alpha <= 45, f"alpha must range between [-10, 45] degrees, current value is {alpha}"
    assert -30 <= beta <= 30, f"beta must range between [-30, 30] degrees, current value is {beta}"
    assert -25 <= deltaE <= 25, f"deltaE must range between [-25, 25] degrees, current value is {deltaE}"
    assert -21.5 <= deltaA <= 21.5, f"deltaA must range between [-21.5, 21.5] degrees, current value is {deltaA}"
    assert -30 <= deltaR <= 30, f"deltaR must range between [-30, 30] degrees, current value is {deltaR}"

    #Degrees to radians conversions.
    alpha = alpha * np.pi / 180
    beta = beta * np.pi / 180
    deltaE = deltaE * np.pi / 180
    deltaA = deltaA * np.pi / 180
    deltaR = deltaR * np.pi / 180

    derivative_dict = {
        'cx': cx(alpha, deltaE),
        'cxQ': cxQ(alpha),
        'cy': cy(beta, deltaA, deltaR),
        'cyP': cyP(alpha),
        'cyR': cyR(alpha),
        'cz': cz(alpha, beta, deltaE),
        'czQ': czQ(alpha),
        'cl': cl(alpha, beta),
        'clP': clP(alpha),
        'clR': clR(alpha),
        'clDeltaA': clDeltaA(alpha, beta),
        'clDeltaR': clDeltaR(alpha, beta),
        'cm': cm(alpha, deltaE),
        'cmQ': cmQ(alpha),
        'cn': cn(alpha, beta),
        'cnP': cnP(alpha),
        'cnR': cnR(alpha),
        'cnDeltaA': cnDeltaA(alpha, beta),
        'cnDeltaR': cnDeltaR(alpha, beta),
        'CL': CL(cx(alpha, deltaE), cz(alpha, beta, deltaE), alpha),
        'CD': CD(cx(alpha, deltaE), cz(alpha, beta, deltaE), alpha)}


    return derivative_dict


def get_aero_forces(density, velocity, alpha, beta, p, q, r, deltaE, deltaA, deltaR):

    coefficients = derivatives(alpha, beta, deltaE, deltaA, deltaR)
    dynamic_pressure = (1 / 2) * density * velocity**2

    #X force.
    CX_total = coefficients['cx'] + (q*CHORD_LENGTH) * coefficients['cxQ'] / (2 * velocity)
    X_force = CX_total * dynamic_pressure * WING_AREA

    #Y force.
    CY_total = coefficients['cy'] + WING_SPAN / (2*velocity) * (coefficients['cyP']*p + coefficients['cyR']*r)
    Y_force = CY_total * dynamic_pressure * WING_AREA

    #Z force.
    CZ_total = coefficients['cz'] + q*coefficients['czQ']*CHORD_LENGTH / (2*velocity)
    Z_force = CZ_total * dynamic_pressure * WING_AREA

    return (X_force, Y_force, Z_force)

def get_aero_moments(density, velocity, alpha, beta, p, q, r, deltaE, deltaA, deltaR):

    coefficients = derivatives(alpha, beta, deltaE, deltaA, deltaR)
    dynamic_pressure = (1/2) * density * velocity**2

    Cm_total = coefficients['cm'] + (coefficients['cmQ'] * CHORD_LENGTH * q) / 2*velocity
    M_moment = Cm_total * dynamic_pressure * WING_AREA * CHORD_LENGTH

    Cl_total = coefficients['cl'] + (coefficients['clP']*p + coefficients['clR']*r) * WING_SPAN / 2*velocity
    L_moment = Cl_total * dynamic_pressure * WING_AREA * WING_SPAN

    Cn_total = coefficients['cn'] + (coefficients['cnP']*p + coefficients['cnR']*r) * WING_SPAN / 2*velocity
    N_moment = Cn_total * dynamic_pressure * WING_AREA * WING_SPAN

    return (L_moment, M_moment, N_moment)
