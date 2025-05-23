import math
import numpy as np
from typing import Optional, Type, Self, Union, List
from Vec3 import Vec3, Vec3Like

type QuatLike = Union[Quat, List[float], np.ndarray]

class Quat(np.ndarray):
    # region SETUP

    # create new object and cast it as a Numpy Array
    def __new__(cls: Type[Self], q:Optional[QuatLike]) -> Self:
        if q:
            return np.asarray(q, dtype=np.float32).view(cls)
        return np.asarray([0, 0, 0,1], dtype=np.float32).view(cls)

    def __array_finalize__(self, obj: Optional[np.ndarray]) -> None:
        if obj is None:
            return

    # override ndarray's str function
    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"Quat( {self[0]}, {self[1]}, {self[2]}, {self[3]} )"

    # endregion

    # region GETTERS / SETTERS

    def copy( self, a: QuatLike )->Self:
        self[ 0 ] = a[ 0 ]
        self[ 1 ] = a[ 1 ]
        self[ 2 ] = a[ 2 ]
        self[ 3 ] = a[ 3 ]
        return self
    
    def clone( self )->"Quat":
        return Quat( self )
    
    # endregion

    # region OPERATIONS

    def mul( self, a: QuatLike )->Self:
        qMul( self, a, self )
        return self
    
    def pmul( self, a: QuatLike )->Self:
        qMul( a, self, self )
        return self

    def norm( self )->Self:
        len =  self[0]**2 + self[1]**2 + self[2]**2 + self[3]**2
        if len > 0:
            len = 1 / math.sqrt( len )
            self[ 0 ] *= len
            self[ 1 ] *= len
            self[ 2 ] *= len
            self[ 3 ] *= len
        return self

    def invert( self )->Self:
        qInvert( self, self )
        return self

    def negate( self )->Self:
        self[ 0 ] = -self[ 0 ]
        self[ 1 ] = -self[ 1 ]
        self[ 2 ] = -self[ 2 ]
        self[ 3 ] = -self[ 3 ]
        return self

    # endregion

    # region FROM OPERATIONS

    def fromMul( self, a: QuatLike, b: QuatLike ) ->Self:
        qMul( a, b, self )
        return self

    def fromInvert( self, q: QuatLike )->Self:
        qInvert( q, self )
        return self
    
    def fromLook( self, fwd: Vec3Like, up: Vec3Like = [0, 1, 0] )->Self:
        # Orthogonal axes to make a mat3x3
        zAxis = Vec3( fwd[0], fwd[1], fwd[2] )
        yAxis = Vec3( up[0], up[1], up[2] )
        xAxis = Vec3().fromCross( yAxis, zAxis ).norm()

        # Z & UP are parallel
        if( xAxis.lenSq == 0 ):
            if abs( yAxis[2] ) == 1:
                zAxis[0] += 0.0001  # shift x when Fwd or Bak
            else:                          
                zAxis[2] += 0.0001  # shift z

            zAxis.norm( zAxis, zAxis )              # ReNormalize updated Fwd
            xAxis.fromCross( yAxis, zAxis ).norm()  # Redo Left
    
        yAxis.fromCross( zAxis, xAxis ).norm() # realign up

        self.fromAxes( xAxis, yAxis, zAxis )
        return self
    
    def fromAxisAngle( self, axis: Vec3Like, rad: float )->Self: 
        half       = rad * 0.5
        s          = math.sin( half )
        self[ 0 ]  = axis[ 0 ] * s
        self[ 1 ]  = axis[ 1 ] * s
        self[ 2 ]  = axis[ 2 ] * s
        self[ 3 ]  = math.cos( half )
        return self

    def fromAxes( self, xAxis: Vec3Like, yAxis: Vec3Like, zAxis: Vec3Like )->Self:
        # Mat3 to Quat
        # Algorithm in Ken Shoemake's article in 1987 SIGGRAPH course notes
        # article "Quat Calculus and Fast Animation".
        m = [*xAxis, *yAxis, *zAxis] # Convert to a Mat3 because conversion uses optimizations related to indexing
        fRoot = 0
        fTrace = m[0] + m[4] + m[8]  # Diagonal axis

        if fTrace > 0.0:
            # |w| > 1/2, may as well choose w > 1/2
            fRoot = math.sqrt(fTrace + 1.0)  # 2w
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

            fRoot = math.sqrt(m[i * 3 + i] - m[j * 3 + j] - m[k * 3 + k] + 1.0)
            self[i] = 0.5 * fRoot
            fRoot = 0.5 / fRoot
            self[3] = (m[j * 3 + k] - m[k * 3 + j]) * fRoot
            self[j] = (m[j * 3 + i] + m[i * 3 + j]) * fRoot
            self[k] = (m[k * 3 + i] + m[i * 3 + k]) * fRoot

        return self
    
    def fromSwing( self, a:Vec3Like, b:Vec3Like )->Self:
        # http://physicsforgames.blogspot.com/2010/03/Quat-tricks.html
        d = Vec3.dot( a, b )

        if d < -0.999999 : # 180 opposites
            tmp = Vec3.cross( [-1,0,0], a )
            if tmp.len < 0.000001 :
                tmp.fromCross( [0,1,0], a )
            
            tmp.norm()

            half      = math.pi * 0.5
            s         = math.sin( half )
            self[ 0 ] = tmp[ 0 ] * s
            self[ 1 ] = tmp[ 1 ] * s
            self[ 2 ] = tmp[ 2 ] * s
            self[ 3 ] = math.cos( half )

        elif( d > 0.999999 ): # Same Direction
            self[ 0 ] = 0
            self[ 1 ] = 0
            self[ 2 ] = 0
            self[ 3 ] = 1
        else:
            v         = Vec3.cross( a, b )
            self[ 0 ] = v[ 0 ]
            self[ 1 ] = v[ 1 ]
            self[ 2 ] = v[ 2 ]
            self[ 3 ] = 1 + d
            
            self.norm()

        return self

    # endregion

    # region SPECIAL OPERATIONS

    # Inverts the quaternion passed in, then pre multiplies to this quaternion.
    # Note: Used often from World to Local space transformation of rotation
    def pmulInvert( self, q: QuatLike )->Self:
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # QUAT INVERT
        ax = q[ 0 ]
        ay = q[ 1 ]
        az = q[ 2 ]
        aw = q[ 3 ]

        d = ax*ax + ay*ay + az*az + aw*aw

        if( d == 0 ):
            ax = ay = az = aw = 0
        else:
            di = 1.0 / d
            ax = -ax * di
            ay = -ay * di
            az = -az * di
            aw =  aw * di

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # QUAT MUL( q, SELF )
        bx = self[ 0 ]
        by = self[ 1 ]
        bz = self[ 2 ]
        bw = self[ 3 ]
        self[ 0 ] = ax * bw + aw * bx + ay * bz - az * by
        self[ 1 ] = ay * bw + aw * by + az * bx - ax * bz
        self[ 2 ] = az * bw + aw * bz + ax * by - ay * bx
        self[ 3 ] = aw * bw - ax * bx - ay * by - az * bz
        return self

    # Test if quat is in the "opposite hemispheres" of another
    # Then negates its if it is. This is used to fix rotation
    # artificats when opposite are mul together. Very noticable
    # when using rotation on skinned vertices then not checked & fixed  
    def dotNegate( self, chk: QuatLike )->Self:
        if Quat.dot( self, chk ) < 0 :
            self[ 0 ] = -self[ 0 ]
            self[ 1 ] = -self[ 1 ]
            self[ 2 ] = -self[ 2 ]
            self[ 3 ] = -self[ 3 ]
        
        return self

    # endregion

    # region STATIC

    def dot( a: QuatLike, b: QuatLike )->float:
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3]

    # endregion


# region REUSABLE OPS
def qMul( a:QuatLike, b:QuatLike, out:QuatLike )-> QuatLike:
    ax = a[0]
    ay = a[1]
    az = a[2]
    aw = a[3]
    bx = b[0] 
    by = b[1] 
    bz = b[2] 
    bw = b[3]
    out[ 0 ] = ax * bw + aw * bx + ay * bz - az * by
    out[ 1 ] = ay * bw + aw * by + az * bx - ax * bz
    out[ 2 ] = az * bw + aw * bz + ax * by - ay * bx
    out[ 3 ] = aw * bw - ax * bx - ay * by - az * bz
    return out

def qInvert( q: QuatLike, out: QuatLike )->QuatLike:
    a0  = q[ 0 ],
    a1  = q[ 1 ],
    a2  = q[ 2 ],
    a3  = q[ 3 ],
    dot = a0*a0 + a1*a1 + a2*a2 + a3*a3

    if dot == 0:
        out[0] = 0
        out[1] = 0
        out[2] = 0
        out[3] = 0 
        return out

    iDot  = 1.0 / dot
    out[ 0 ] = -a0 * iDot
    out[ 1 ] = -a1 * iDot
    out[ 2 ] = -a2 * iDot
    out[ 3 ] =  a3 * iDot
    return out
# endregion