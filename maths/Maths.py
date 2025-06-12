from .types import Vec3Like
import math
import numpy as np


def fract(f: float) -> float:
    return f - np.floor(f)


def snap(x: float, step: float) -> float:
    return np.floor(x / step) * step


# Adapted from GODOT-engine math_funcs.h
def wrap(value: float, min: float, max: float) -> float:
    range = max - min
    if range != 0:
        return value - (range * np.floor((value - min) / range))
    return min


def norm(minv: float, maxv: float, v: float) -> float:
    return (v - minv) / (maxv - minv)


def spherical(x: float, y: float) -> Vec3Like:
    sx = np.sin(x)
    return [
        np.sin(y) * sx,
        np.cos(x),
        np.cos(y) * sx,
    ]


# ts = np.zeros(clip.frameCount, dtype=np.float32)
