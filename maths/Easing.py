import numpy as np


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def quad_in(k: float) -> float:
    return k * k


def quad_out(k: float) -> float:
    return k * (2 - k)


def quad_inout(k: float) -> float:
    k = k * 2
    if k < 1:
        return 0.5 * k * k

    k = k - 1
    return -0.5 * (k * (k - 2) - 1)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def cubic_in(k: float) -> float:
    return k * k * k


def cubic_out(k: float) -> float:
    k = k - 1
    return k * k * k + 1


def cubic_inout(k: float) -> float:
    k = k * 2
    if k < 1:
        return 0.5 * k * k * k

    k = k - 2
    return 0.5 * (k * k * k + 2)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def quart_in(k: float) -> float:
    return k * k * k * k


def quart_out(k: float) -> float:
    k = k - 1
    return 1 - (k * k * k * k)


def quart_inout(k: float) -> float:
    k = k * 2
    if k < 1:
        return 0.5 * k * k * k * k

    k = k - 2
    return -0.5 * (k * k * k * k - 2)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def quint_in(k: float) -> float:
    return k * k * k * k * k


def quint_out(k: float) -> float:
    k = k - 1
    return k * k * k * k * k + 1


def quint_inout(k: float) -> float:
    k = k * 2
    if k < 1:
        return 0.5 * k * k * k * k * k

    k = k - 2
    return 0.5 * (k * k * k * k * k + 2)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def sine_in(k: float) -> float:
    return 1 - np.cos(k * np.pi / 2)


def sine_out(k: float) -> float:
    return np.sin(k * np.pi / 2)


def sine_inout(k: float) -> float:
    return 0.5 * (1 - np.cos(np.pi * k))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def exp_in(k: float) -> float:
    if k == 0:
        return 0

    return np.pow(1024, k - 1)


def exp_out(k: float) -> float:
    if k == 1:
        return 1
    return 1 - np.pow(2, -10 * k)


def exp_inout(k: float) -> float:
    if k == 0 or k == 1:
        return k

    k = k * 2
    if k < 1:
        return 0.5 * np.pow(1024, k - 1)

    return 0.5 * (-np.pow(2, -10 * (k - 1)) + 2)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def circ_in(k: float) -> float:
    return 1 - np.sqrt(1 - k * k)


def circ_out(k: float) -> float:
    k = k - 1
    return np.sqrt(1 - (k * k))


def circ_inout(k: float) -> float:
    k = k * 2
    if k < 1:
        return -0.5 * (np.sqrt(1 - k * k) - 1)

    k = k - 2
    return 0.5 * (np.sqrt(1 - k * k) + 1)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def elastic_in(k: float) -> float:
    if k == 0 or k == 1:
        return k
    return -np.pow(2, 10 * (k - 1)) * np.sin((k - 1.1) * 5 * np.pi)


def elastic_out(k: float) -> float:
    if k == 0 or k == 1:
        return k

    return np.pow(2, -10 * k) * np.sin((k - 0.1) * 5 * np.pi) + 1


def elastic_inout(k: float) -> float:
    if k == 0 or k == 1:
        return k

    k = k * 2
    if k < 1:
        return -0.5 * np.pow(2, 10 * (k - 1)) * np.sin((k - 1.1) * 5 * np.pi)

    return 0.5 * np.pow(2, -10 * (k - 1)) * np.sin((k - 1.1) * 5 * np.pi) + 1


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def back_in(k: float) -> float:
    return k * k * ((1.70158 + 1) * k - 1.70158)


def back_out(k: float) -> float:
    k = k - 1
    return k * k * ((1.70158 + 1) * k + 1.70158) + 1


def back_inout(k: float) -> float:
    s = 1.70158 * 1.525
    k = k * 2
    if k < 1:
        return 0.5 * (k * k * ((s + 1) * k - s))

    k = k - 2
    return 0.5 * (k * k * ((s + 1) * k + s) + 2)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def bounce_in(k: float) -> float:
    return 1 - bounce_out(1 - k)


def bounce_out(k: float) -> float:
    if k < (1 / 2.75):
        return 7.5625 * k * k
    elif k < (2 / 2.75):
        k = k - (1.5 / 2.75)
        return 7.5625 * k * k + 0.75
    elif k < (2.5 / 2.75):
        k = k - (2.25 / 2.75)
        return 7.5625 * k * k + 0.9375
    else:
        k = k - (2.625 / 2.75)
        return 7.5625 * k * k + 0.984375


def bounce_inout(k: float) -> float:
    if k < 0.5:
        return bounce_in(k * 2) * 0.5

    return bounce_out(k * 2 - 1) * 0.5 + 0.5


def bounce(t: float) -> float:
    return (np.sin(t * np.pi * (0.2 + 2.5 * t * t * t)) * np.pow(1 - t, 2.2) + t) * (
        1 + (1.2 * (1 - t))
    )
