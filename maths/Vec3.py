from typing import Optional, Type, Self, Union, Tuple
from .types import Vec3Like, QuatLike

import math
import numpy as np


class Vec3(np.ndarray):
    # region SETUP

    # create new object and cast it as a Numpy Array
    def __new__(cls: Type[Self], x: float = 0.0, y: float = 0.0, z: float = 0.0) -> Self:
        obj = np.asarray([x, y, z], dtype=np.float32).view(cls)
        return obj

    def __array_finalize__(self, obj: Optional[np.ndarray]) -> None:
        if obj is None:
            return

    # override ndarray's str function
    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"[{self[0]}, {self[1]}, {self[2]}]"

    # endregion

    # region GETTERS / SETTERS

    @property
    def x(self) -> float:
        return self[0]

    @x.setter
    def x(self, v: float) -> None:
        self[0] = v

    @property
    def y(self) -> float:
        return self[1]

    @y.setter
    def y(self, v: float) -> None:
        self[1] = v

    @property
    def z(self: float) -> float:
        return self[2]

    @z.setter
    def z(self, v: float) -> None:
        self[2] = v

    @property
    def len(self) -> float:
        return math.sqrt(self[0] ** 2 + self[1] ** 2 + self[2] ** 2)

    @property
    def lenSq(self) -> float:
        return self[0] ** 2 + self[1] ** 2 + self[2] ** 2

    def copy(self, a: Vec3Like) -> Self:
        self[0] = a[0]
        self[1] = a[1]
        self[2] = a[2]
        return self

    def clone(self) -> "Vec3":
        return Vec3(self[0], self[1], self[2])

    # endregion

    # region DUNDER METHODS

    # vc = va + vb,  vc = va + [1,2,3]
    def __add__(self, v: Vec3Like) -> Self:
        return Vec3(self[0] + v[0], self[1] + v[1], self[2] + v[2])

    # va += vb,  va += [1,2,3]
    def __iadd__(self, v: Vec3Like) -> Self:
        self[0] += v[0]
        self[1] += v[1]
        self[2] += v[2]
        return self

    # vc = va - vb,  vc = va - [1,2,3]
    def __sub__(self, v: Vec3Like) -> Self:
        return Vec3(self[0] - v[0], self[1] - v[1], self[2] - v[2])

    # va -= vb,  va -= [1,2,3]
    def __isub__(self, v: Vec3Like) -> Self:
        self[0] -= v[0]
        self[1] -= v[1]
        self[2] -= v[2]
        return self

    # vc = va * vb, vc = va * [1,2,3],  vc = va * 5
    def __mul__(self, v: Union[float, Vec3Like]) -> Self:
        if isinstance(v, (int, float)):
            return Vec3(self[0] * v, self[1] * v, self[2] * v)

        elif isinstance(v, (Vec3, list)):

            if len(v) < 3:
                raise ValueError(
                    "Vec3Like object must have at least 3 components for multiplication."
                )

            return Vec3(self[0] * v[0], self[1] * v[1], self[2] * v[2])
        else:
            return NotImplemented  # Allow Python to try other options if type is not supported

    # va *= vb, va *= [1,2,3],  va *= 5
    def __imul__(self, v: Union[float, Vec3Like]) -> Self:
        if isinstance(v, (int, float)):
            self[0] *= v
            self[1] *= v
            self[2] *= v
        elif isinstance(v, (Vec3, list)):
            if len(v) < 3:
                raise ValueError("Vec3like object must have at least 3 components for mul")

            self[0] *= v[0]
            self[1] *= v[1]
            self[2] *= v[2]
        else:
            return NotImplemented

        return self

    # vc = 5 * va
    def __rmul__(self, v: float) -> Self:
        if isinstance(v, (int, float)):
            return self.__mul__(v)
        else:
            return NotImplemented

    # endregion

    # region OPERATIONS

    def add(self, v: Vec3Like) -> Self:
        self[0] += v[0]
        self[1] += v[1]
        self[2] += v[2]

        return self

    def sub(self, v: Vec3Like) -> Self:
        self[0] -= v[0]
        self[1] -= v[1]
        self[2] -= v[2]

        return self

    def mul(self, v: Vec3Like) -> Self:
        self[0] *= v[0]
        self[1] *= v[1]
        self[2] *= v[2]

        return self

    def scale(self, s: Union[int, float]) -> Self:
        self[0] *= s
        self[1] *= s
        self[2] *= s

        return self

    def norm(self) -> Self:
        mag = math.sqrt(self[0] ** 2 + self[1] ** 2 + self[2] ** 2)
        if mag == 0:
            return self

        mag = 1 / mag
        self[0] *= mag
        self[1] *= mag
        self[2] *= mag
        return self

    def negate(self) -> Self:
        self[0] = -self[0]
        self[1] = -self[1]
        self[2] = -self[2]
        return self

    def quatTransform(self, q: QuatLike) -> Self:
        qx = q[0]
        qy = q[1]
        qz = q[2]
        qw = q[3]
        vx = self[0]
        vy = self[1]
        vz = self[2]
        x1 = qy * vz - qz * vy
        y1 = qz * vx - qx * vz
        z1 = qx * vy - qy * vx
        x2 = qw * x1 + qy * z1 - qz * y1
        y2 = qw * y1 + qz * x1 - qx * z1
        z2 = qw * z1 + qx * y1 - qy * x1
        self[0] = vx + 2 * x2
        self[1] = vy + 2 * y2
        self[2] = vz + 2 * z2
        return self

    # endregion

    # region FROM OPERATORS

    def fromAdd(self, a: Vec3Like, b: Vec3Like) -> Self:
        self[0] = a[0] + b[0]
        self[1] = a[1] + b[1]
        self[2] = a[2] + b[2]
        return self

    def fromMul(self, a: Vec3Like, b: Vec3Like) -> Self:
        self[0] = a[0] * b[0]
        self[1] = a[1] * b[1]
        self[2] = a[2] * b[2]
        return self

    def fromInvert(self, a: Vec3Like) -> Self:
        self[0] = 1 / a[0]
        self[1] = 1 / a[1]
        self[2] = 1 / a[2]
        return self

    def fromNegate(self, a: Vec3Like) -> Self:
        self[0] = -a[0]
        self[1] = -a[1]
        self[2] = -a[2]
        return self

    def fromCross(self, a: Vec3Like, b: Vec3Like) -> Self:
        ax = a[0]
        ay = a[1]
        az = a[2]
        bx = b[0]
        by = b[1]
        bz = b[2]

        self[0] = ay * bz - az * by
        self[1] = az * bx - ax * bz
        self[2] = ax * by - ay * bx
        return self

    def fromLerp(self, a: Vec3Like, b: Vec3Like, t: float) -> Self:
        ti = 1 - t
        self[0] = a[0] * ti + b[0] * t
        self[1] = a[1] * ti + b[1] * t
        self[2] = a[2] * ti + b[2] * t
        return self

    def fromScaleThenAdd(self, s: float, v: Vec3Like, a: Vec3Like) -> Self:
        self[0] = v[0] * s + a[0]
        self[1] = v[1] * s + a[1]
        self[2] = v[2] * s + a[2]
        return self

    def fromQuat(self, q: QuatLike, v: Vec3Like) -> Self:
        qx = q[0]
        qy = q[1]
        qz = q[2]
        qw = q[3]
        vx = v[0]
        vy = v[1]
        vz = v[2]
        x1 = qy * vz - qz * vy
        y1 = qz * vx - qx * vz
        z1 = qx * vy - qy * vx
        x2 = qw * x1 + qy * z1 - qz * y1
        y2 = qw * y1 + qz * x1 - qx * z1
        z2 = qw * z1 + qx * y1 - qy * x1
        self[0] = vx + 2 * x2
        self[1] = vy + 2 * y2
        self[2] = vz + 2 * z2
        return self

    # endregion

    # region STATIC OPERATIONS

    def dot(a: Vec3Like, b: Vec3Like) -> Self:
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    def cross(a: Vec3Like, b: Vec3Like) -> "Vec3":
        return Vec3(a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

    def dist(a: Vec3Like, b: Vec3Like) -> float:
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)

    def distSq(a: Vec3Like, b: Vec3Like) -> float:
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2

    def orthogonal(fwd: Vec3Like, up: Vec3Like = [0, 1, 0]) -> Tuple["Vec3", "Vec3", "Vec3"]:
        zAxis = Vec3(fwd[0], fwd[1], fwd[2])
        yAxis = Vec3(up[0], up[1], up[2])
        xAxis = Vec3().fromCross(yAxis, zAxis).norm()

        # Z & UP are parallel
        if xAxis.lenSq == 0:
            if abs(yAxis[2]) == 1:
                zAxis[0] += 0.0001  # shift x when Fwd or Bak
            else:
                zAxis[2] += 0.0001  # shift z

            zAxis.norm(zAxis, zAxis)  # ReNormalize updated Fwd
            xAxis.fromCross(yAxis, zAxis).norm()  # Redo Left

        yAxis.fromCross(zAxis, xAxis).norm()  # realign up
        return [xAxis, yAxis, zAxis]

    # endregion
