import numpy as np

"""
http://paulbourke.net/miscellaneous/interpolation/

Lagrange Interpolation
- https://www.youtube.com/watch?v=4S6G-zenbFM
- https://www.geeksforgeeks.org/lagranges-interpolation/
"""

# region MISC


def linear(a: float, b: float, t: float) -> float:
    return a * (1 - t) + b * t


# @FreyaHolmer : exponential interpolation, if you want to find the frequency,
# zoom level or scale, halfway between 2 and 8, then the right answer is 4, not 5
def eerp(a: float, b: float, t: float) -> float:
    return a ** (1 - t) * b**t


# CLerp - Circular Lerp - is like lerp but handles the wraparound from 0 to 360.
# This is useful when interpolating eulerAngles and the object crosses the 0/360 boundary.
# http://wiki.unity3d.com/index.php/Mathfx#C.23_-_Mathfx.cs
def clerp(start: float, end: float, v: float) -> float:
    min = 0.0
    max = 360.0
    half = np.abs((max - min) / 2.0)  # half the distance between min and max
    es = end - start

    if es < -half:
        return start + (((max - start) + end) * v)
    elif es > half:
        return start + (-((max - end) + start) * v)

    return start + es * v


# http://paulbourke.net/miscellaneous/interpolation/
def cosine(a: float, b: float, t: float) -> float:
    t2 = (1 - np.cos(t * np.PI)) / 2
    return a * (1 - t2) + b * t2


# endregion


# region CURVE BASED


# http://archive.gamedev.net/archive/reference/articles/article1497.html
def cubic(a: float, b: float, t: float) -> float:
    t2 = t * t
    t3 = t2 * t
    return a * (2 * t3 - 3 * t2 + 1) + b * (3 * t2 - 2 * t3)


# http://paulbourke.net/miscellaneous/interpolation/
def cubicSpline(a: float, b: float, c: float, d: float, t: float) -> float:
    t2 = t * t
    a0 = d - c - a + b
    a1 = a - b - a0
    a2 = c - a
    return a0 * t * t2 + a1 * t2 + a2 * t + b


# catmull - http://paulbourke.net/miscellaneous/interpolation/
def cubicSmooth(a: float, b: float, c: float, d: float, t: float) -> float:
    t2 = t * t
    a0 = -0.5 * a + 1.5 * b - 1.5 * c + 0.5 * d
    a1 = a - 2.5 * b + 2 * c - 0.5 * d
    a2 = -0.5 * a + 0.5 * c
    return a0 * t * t2 + a1 * t2 + a2 * t + b


def hermite(a: float, b: float, c: float, d: float, t: float, tension: float, bias: float) -> float:
    """
    Tension : 1 is high, 0 normal, -1 is low
    Bias    : 0 is even,
                positive is towards first segment,
                negative towards the other
    """
    t2 = t * t
    t3 = t2 * t
    btPN = (1 + bias) * (1 - tension) / 2
    btNP = (1 - bias) * (1 - tension) / 2
    m0 = (b - a) * btPN + (c - b) * btNP
    m1 = (c - b) * btPN + (d - c) * btNP
    a0 = 2 * t3 - 3 * t2 + 1
    a1 = t3 - 2 * t2 + t
    a2 = t3 - t2
    a3 = -2 * t3 + 3 * t2
    return a0 * b + a1 * m0 + a2 * m1 + a3 * c


# endregion
