import numpy as np


def p_q_solve(a: float, b: float, c: float) -> tuple:
    """
    p_q_solve computes the zeroes of a quadratic function.

    Parameters
    ----------
    a : float
        Factor of quadratic x-term
    b : float
        Factor of single x-term
    c : float
        Constant

    Returns
    -------
    tuple
        Zeroes
    """
    try:
        nst_1 = -(b / (2 * a)) + np.sqrt((b / (2 * a)) ** 2 - (c / a))
    except BaseException:
        print("prob. complex")
        nst_1 = None
    try:
        nst_2 = -(b / (2 * a)) - np.sqrt((b / (2 * a)) ** 2 - (c / a))
    except BaseException:
        nst_2 = None
        print("prob. complex")

    return nst_1, nst_2