from IPython.display import Latex
from IPython import display
import numpy as np


def print_matrix(A: np.ndarray, name: str) -> None:
    """
    print_matrix renders a given matrix to the LaTeX matrix notation.

    Parameters
    ----------
    A : np.ndarray
        Matrix
    name : str
        Variable name
    """
    latex = r"\begin{equation*}\mathbf{%s}=\begin{pmatrix}" % (name)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            real = np.round(np.real(A[i, j]))
            imag = np.round(np.imag(A[i, j]))
        if real > 0:
            latex += "%d" % (real)
        elif real < 0:
            latex += "-%d" % (-real)
        if real != 0 and imag > 0:
            latex += "+"
        if imag > 0:
            latex += "%d\mathrm{j}" % (imag)
        elif imag < 0:
            latex += "-%d\mathrm{j}" % (-imag)
        if real == 0 and imag == 0:
            latex += "0"
        if j == A.shape[1] - 1:
            latex += r"\\"
        else:
            latex += " & "
    latex += r"\end{pmatrix}\end{equation*}"
    display(Latex(latex))
