import numpy as np


def circ_conv(sign_1: np.ndarray, sign_2: np.ndarray) -> np.ndarray:
    """
    circ_conv computes the circular convolution.

    Parameters
    ----------
    sign_1 : np.ndarray
        Real valued 1D array
    sign_2 : np.ndarray
        Real valued 1D array

    Returns
    -------
    np.ndarray
        Circular convolution
    """
    return np.real(np.fft.ifft(np.fft.fft(sign_1) * np.fft.fft(sign_2)))
