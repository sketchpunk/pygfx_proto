from typing import Optional, Type, Self
from .types import Vec3Like, QuatLike
from numpy.typing import NDArray

import math
import numpy as np
from .Vec3 import Vec3


class Quat(np.ndarray):
    # region SETUP

    # create new object and cast it as a Numpy Array
    def __new__(cls: Type[Self], q: Optional[QuatLike] = None) -> Self:
        if q:
            return np.asarray(q, dtype=np.float32).view(cls)
        return np.asarray([0, 0, 0, 1], dtype=np.float32).view(cls)

    def __array_finalize__(self, obj: Optional[np.ndarray]) -> None:
        if obj is None:
            return

    # override ndarray's str function
    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"[{self[0]}, {self[1]}, {self[2]}, {self[3]}]"

    # endregion

    # region GETTERS / SETTERS

    def copy(self, a: QuatLike) -> Self:
        self[0] = a[0]
        self[1] = a[1]
        self[2] = a[2]
        self[3] = a[3]
        return self

    def copyTo(self, a: QuatLike) -> Self:
        a[0] = self[0]
        a[1] = self[1]
        a[2] = self[2]
        a[3] = self[3]
        return self

    def clone(self) -> "Quat":
        return Quat(self)

    # endregion

    # region OPERATIONS

    def mul(self, a: QuatLike) -> Self:
        qMul(self, a, self)
        return self

    def pmul(self, a: QuatLike) -> Self:
        qMul(a, self, self)
        return self

    def norm(self) -> Self:
        len = self[0] ** 2 + self[1] ** 2 + self[2] ** 2 + self[3] ** 2
        if len > 0:
            len = 1 / np.sqrt(len)
            self[0] *= len
            self[1] *= len
            self[2] *= len
            self[3] *= len
        return self

    def invert(self) -> Self:
        qInvert(self, self)
        return self

    def negate(self) -> Self:
        self[0] = -self[0]
        self[1] = -self[1]
        self[2] = -self[2]
        self[3] = -self[3]
        return self

    # endregion

    # region FROM OPERATIONS

    def fromMul(self, a: QuatLike, b: QuatLike) -> Self:
        qMul(a, b, self)
        return self

    def fromInvert(self, q: QuatLike) -> Self:
        qInvert(q, self)
        return self

    def fromLook(self, fwd: Vec3Like, up: Vec3Like = [0, 1, 0]) -> Self:
        # Orthogonal axes to make a mat3x3
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

        self.fromAxes(xAxis, yAxis, zAxis)
        return self

    def fromAxisAngle(self, axis: Vec3Like, rad: float) -> Self:
        half = rad * 0.5
        s = math.sin(half)
        self[0] = axis[0] * s
        self[1] = axis[1] * s
        self[2] = axis[2] * s
        self[3] = math.cos(half)
        return self

    def fromAxes(self, xAxis: Vec3Like, yAxis: Vec3Like, zAxis: Vec3Like) -> Self:
        # Mat3 to Quat
        # Algorithm in Ken Shoemake's article in 1987 SIGGRAPH course notes
        # article "Quat Calculus and Fast Animation".
        m = [
            *xAxis,
            *yAxis,
            *zAxis,
        ]  # Convert to a Mat3 because conversion uses optimizations related to indexing
        fRoot = 0
        fTrace = m[0] + m[4] + m[8]  # Diagonal axis

        if fTrace > 0.0:
            # |w| > 1/2, may as well choose w > 1/2
            fRoot = np.sqrt(fTrace + 1.0)  # 2w
            self[3] = 0.5 * fRoot

            fRoot = 0.5 / fRoot  # 1/(4w)
            self[0] = (m[5] - m[7]) * fRoot
            self[1] = (m[6] - m[2]) * fRoot
            self[2] = (m[1] - m[3]) * fRoot
        else:
            # |w| <= 1/2
            i = 0
            if m[4] > m[0]:
                i = 1
            if m[8] > m[i * 3 + i]:
                i = 2

            j = (i + 1) % 3
            k = (i + 2) % 3

            fRoot = np.sqrt(m[i * 3 + i] - m[j * 3 + j] - m[k * 3 + k] + 1.0)
            self[i] = 0.5 * fRoot
            fRoot = 0.5 / fRoot
            self[3] = (m[j * 3 + k] - m[k * 3 + j]) * fRoot
            self[j] = (m[j * 3 + i] + m[i * 3 + j]) * fRoot
            self[k] = (m[k * 3 + i] + m[i * 3 + k]) * fRoot

        return self

    def fromSwing(self, a: Vec3Like, b: Vec3Like) -> Self:
        # http://physicsforgames.blogspot.com/2010/03/Quat-tricks.html
        d = Vec3.dot(a, b)

        if d < -0.999999:  # 180 opposites
            tmp = Vec3.cross([-1, 0, 0], a)
            if tmp.len < 0.000001:
                tmp.fromCross([0, 1, 0], a)

            tmp.norm()

            half = math.pi * 0.5
            s = math.sin(half)
            self[0] = tmp[0] * s
            self[1] = tmp[1] * s
            self[2] = tmp[2] * s
            self[3] = math.cos(half)

        elif d > 0.999999:  # Same Direction
            self[0] = 0
            self[1] = 0
            self[2] = 0
            self[3] = 1
        else:
            v = Vec3.cross(a, b)
            self[0] = v[0]
            self[1] = v[1]
            self[2] = v[2]
            self[3] = 1 + d

            self.norm()

        return self

    def fromEulerOrder(self, x: float, y: float, z: float, order: str = "YXZ") -> Self:
        # https://github.com/mrdoob/three.js/blob/dev/src/math/Quat.js
        c1 = np.cos(x * 0.5)
        c2 = np.cos(y * 0.5)
        c3 = np.cos(z * 0.5)
        s1 = np.sin(x * 0.5)
        s2 = np.sin(y * 0.5)
        s3 = np.sin(z * 0.5)

        match order:
            case "XYZ":
                self[0] = s1 * c2 * c3 + c1 * s2 * s3
                self[1] = c1 * s2 * c3 - s1 * c2 * s3
                self[2] = c1 * c2 * s3 + s1 * s2 * c3
                self[3] = c1 * c2 * c3 - s1 * s2 * s3
            case "YXZ":
                self[0] = s1 * c2 * c3 + c1 * s2 * s3
                self[1] = c1 * s2 * c3 - s1 * c2 * s3
                self[2] = c1 * c2 * s3 - s1 * s2 * c3
                self[3] = c1 * c2 * c3 + s1 * s2 * s3
            case "ZXY":
                self[0] = s1 * c2 * c3 - c1 * s2 * s3
                self[1] = c1 * s2 * c3 + s1 * c2 * s3
                self[2] = c1 * c2 * s3 + s1 * s2 * c3
                self[3] = c1 * c2 * c3 - s1 * s2 * s3
            case "ZYX":
                self[0] = s1 * c2 * c3 - c1 * s2 * s3
                self[1] = c1 * s2 * c3 + s1 * c2 * s3
                self[2] = c1 * c2 * s3 - s1 * s2 * c3
                self[3] = c1 * c2 * c3 + s1 * s2 * s3
            case "YZX":
                self[0] = s1 * c2 * c3 + c1 * s2 * s3
                self[1] = c1 * s2 * c3 + s1 * c2 * s3
                self[2] = c1 * c2 * s3 - s1 * s2 * c3
                self[3] = c1 * c2 * c3 - s1 * s2 * s3
            case "XZY":
                self[0] = s1 * c2 * c3 - c1 * s2 * s3
                self[1] = c1 * s2 * c3 - s1 * c2 * s3
                self[2] = c1 * c2 * s3 + s1 * s2 * c3
                self[3] = c1 * c2 * c3 + s1 * s2 * s3

        return self.norm()

    # endregion

    # region SPECIAL OPERATIONS

    # Inverts the quaternion passed in, then pre multiplies to this quaternion.
    # Note: Used often from World to Local space transformation of rotation
    def pmulInvert(self, q: QuatLike) -> Self:
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # QUAT INVERT
        ax = q[0]
        ay = q[1]
        az = q[2]
        aw = q[3]

        d = ax * ax + ay * ay + az * az + aw * aw

        if d == 0:
            ax = ay = az = aw = 0
        else:
            di = 1.0 / d
            ax = -ax * di
            ay = -ay * di
            az = -az * di
            aw = aw * di

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # QUAT MUL( q, SELF )
        bx = self[0]
        by = self[1]
        bz = self[2]
        bw = self[3]
        self[0] = ax * bw + aw * bx + ay * bz - az * by
        self[1] = ay * bw + aw * by + az * bx - ax * bz
        self[2] = az * bw + aw * bz + ax * by - ay * bx
        self[3] = aw * bw - ax * bx - ay * by - az * bz
        return self

    # Test if quat is in the "opposite hemispheres" of another
    # Then negates its if it is. This is used to fix rotation
    # artificats when opposite are mul together. Very noticable
    # when using rotation on skinned vertices then not checked & fixed
    def dotNegate(self, chk: QuatLike) -> Self:
        if Quat.dot(self, chk) < 0:
            self[0] = -self[0]
            self[1] = -self[1]
            self[2] = -self[2]
            self[3] = -self[3]

        return self

    # endregion

    # region STATIC

    def dot(a: QuatLike, b: QuatLike) -> float:
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3]

    def slerp(a: QuatLike, b: QuatLike, t: float, out: QuatLike = [0, 0, 0, 1]) -> QuatLike:
        # benchmarks: http://jsperf.com/Quat-slerp-implementations
        ax = a[0]
        ay = a[1]
        az = a[2]
        aw = a[3]
        bx = b[0]
        by = b[1]
        bz = b[2]
        bw = b[3]

        # let omega, cosom, sinom,
        scale0 = 0
        scale1 = 1

        # calc cosine
        cosom = ax * bx + ay * by + az * bz + aw * bw

        # adjust signs (if necessary)
        if cosom < 0.0:
            cosom = -cosom
            bx = -bx
            by = -by
            bz = -bz
            bw = -bw

        # calculate coefficients
        if (1.0 - cosom) > 0.000001:
            # standard case (slerp)
            omega = np.acos(cosom)
            sinom = np.sin(omega)
            scale0 = np.sin((1.0 - t) * omega) / sinom
            scale1 = np.sin(t * omega) / sinom
        else:
            # "from" and "to" Quats are very close so we can do a linear interpolation
            scale0 = 1.0 - t
            scale1 = t

        # calculate final values
        out[0] = scale0 * ax + scale1 * bx
        out[1] = scale0 * ay + scale1 * by
        out[2] = scale0 * az + scale1 * bz
        out[3] = scale0 * aw + scale1 * bw

        return out

    # Cheaper alternative to slerp
    def nblend(a: QuatLike, b: QuatLike, t: float, out: QuatLike = [0, 0, 0, 1]) -> QuatLike:
        # https://physicsforgames.blogspot.com/2010/02/quaternions.html
        a_x = a[0]  # Quaternion From
        a_y = a[1]
        a_z = a[2]
        a_w = a[3]
        b_x = b[0]  # Quaternion To
        b_y = b[1]
        b_z = b[2]
        b_w = b[3]
        dot = a_x * b_x + a_y * b_y + a_z * b_z + a_w * b_w
        ti = 1 - t
        s = 1

        # if Rotations with a dot less then 0 causes artifacts when lerping,
        # Can fix this by switching the sign of the To Quaternion.
        if dot < 0:
            s = -1

        out[0] = ti * a_x + t * b_x * s
        out[1] = ti * a_y + t * b_y * s
        out[2] = ti * a_z + t * b_z * s
        out[3] = ti * a_w + t * b_w * s

        return qNorm(out, out)

    def createBuffer(cnt: int, init: QuatLike = [0, 0, 0, 1]) -> NDArray[np.float32]:
        return np.full((cnt, 4), init, dtype=np.float32)

    # endregion


# region REUSABLE OPS


def qMul(a: QuatLike, b: QuatLike, out: QuatLike) -> QuatLike:
    ax = a[0]
    ay = a[1]
    az = a[2]
    aw = a[3]
    bx = b[0]
    by = b[1]
    bz = b[2]
    bw = b[3]
    out[0] = ax * bw + aw * bx + ay * bz - az * by
    out[1] = ay * bw + aw * by + az * bx - ax * bz
    out[2] = az * bw + aw * bz + ax * by - ay * bx
    out[3] = aw * bw - ax * bx - ay * by - az * bz
    return out


def qInvert(q: QuatLike, out: QuatLike) -> QuatLike:
    a0 = (q[0],)
    a1 = (q[1],)
    a2 = (q[2],)
    a3 = (q[3],)
    dot = a0 * a0 + a1 * a1 + a2 * a2 + a3 * a3

    if dot == 0:
        out[0] = 0
        out[1] = 0
        out[2] = 0
        out[3] = 0
        return out

    iDot = 1.0 / dot
    out[0] = -a0 * iDot
    out[1] = -a1 * iDot
    out[2] = -a2 * iDot
    out[3] = a3 * iDot
    return out


def qNorm(a: QuatLike, out: QuatLike = [0, 0, 0, 1]) -> QuatLike:
    len = a[0] ** 2 + a[1] ** 2 + a[2] ** 2 + a[3] ** 2
    if len > 0:
        len = 1 / np.sqrt(len)
        out[0] = a[0] * len
        out[1] = a[1] * len
        out[2] = a[2] * len
        out[3] = a[3] * len
    return out


# endregion
