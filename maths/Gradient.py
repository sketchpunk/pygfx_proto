import numpy as np
from .Maths import fract

# region STEP


def step(edge: float, x: float) -> float:
    if x < edge:
        return 0
    return 1


# t must be in the range of 0 to 1 : start & ends slowly
def smoothTStep(t: float) -> float:
    return t * t * (3 - 2 * t)


def smoothStep(min: float, max: float, v: float) -> float:
    # https://en.wikipedia.org/wiki/Smoothstep
    v = np.max(0, np.min(1, (v - min) / (max - min)))
    return v * v * (3 - 2 * v)


def smootherStep(min: float, max: float, v: float) -> float:
    if v <= min:
        return 0
    if v >= max:
        return 1

    v = (v - min) / (max - min)
    return v * v * v * (v * (v * 6 - 15) + 10)


# endregion

# region MISC


# See: https://www.iquilezles.org/www/articles/smin/smin.htm
def smoothMin(a: float, b: float, k: float) -> float:
    if k != 0:
        h = np.max(k - np.abs(a - b), 0.0) / k
        return np.min(a, b) - h * h * h * k * (1 / 6)

    return np.min(a, b)


def fade(t: float) -> float:
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


# Remap 0 > 1 to -1 > 0 > 1
def remapN01(t: float) -> float:
    return t * 2 - 1


# Remap 0 > 1 to 0 > 1 > 0
def remap010(t: float) -> float:
    return 1 - np.abs(2 * t - 1)


def noise(x: float) -> float:
    # <https://www.shadertoy.com/view/4dS3Wd> By Morgan McGuire @morgan3d, http://graphicscodex.com
    # https://gist.github.com/patriciogonzalezvivo/670c22f3966e662d2f83
    i = np.floor(x)
    f = fract(x)
    t = f * f * (3 - 2 * f)
    return fract(np.sin(i) * 1e4) * (1 - t) + fract(np.sin(i + 1.0) * 1e4) * t


def bouncy(t: float, jump: float = 6, offset: float = 1) -> float:
    rad = 6.283185307179586 * t  # PI_2 * t
    return (offset + np.sin(rad)) / 2 * np.sin(jump * rad)


# This is a smooth over-shoot easing : t must be in the range of 0 to 1
def overShoot(t: float, n: float = 2, k: float = 2) -> float:
    # https://www.youtube.com/watch?v=pydKWTSGMEM
    t = t * t * (3 - 2 * t)  # SmoothTStep to smooth out the starting & end
    a = n * t * t
    b = 1 - k * ((t - 1) ** 2)
    return a * (1 - t) + b * t


# endregion

# region CURVES


# Over 0, Eases in the middle, under eases in-out
def sigmoid(t: float, k: float = 0) -> float:
    # this uses the -1 to 1 value of sigmoid which allows to create easing at
    # start and finish. Can pass in range 0:1 and it'll return that range.
    # https://dhemery.github.io/DHE-Modules/technical/sigmoid/
    # https://www.desmos.com/calculator/q6ukniiqwn
    return (t - k * t) / (k - 2 * k * np.abs(t) + 1)


def parabola(x: float, k: float) -> float:
    return np.pow(4 * x * (1 - x), k)


def bellCurve(t: float) -> float:
    return (np.sin(2 * np.pi * (t - 0.25)) + 1) * 0.5


# a = 1.5, 2, 4, 9
def betaDistCurve(t: float, a: float) -> float:
    # https://stackoverflow.com/questions/13097005/easing-functions-for-bell-curves
    return 4**a * (t * (1 - t)) ** a


# endregion
