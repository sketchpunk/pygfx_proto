from .types import Vec3Like
import math


def fNorm(minv: float, maxv: float, v: float) -> float:
    return (v - minv) / (maxv - minv)


def smoothStep(minv, maxv, v) -> float:
    # https://en.wikipedia.org/wiki/Smoothstep
    v = max(0, min(1, (v - minv) / (maxv - minv)))
    return v * v * (3 - 2 * v)


def spherical(x: float, y: float) -> Vec3Like:
    sx = math.sin(x)
    return [
        math.sin(y) * sx,
        math.cos(x),
        math.cos(y) * sx,
    ]
