from jatools import p_q_solve

def test_p_q_solve()->None:
    p,q = p_q_solve(1,-2,0)
    assert p,q == (2.0, 0.0)
    