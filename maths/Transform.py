from typing import Optional, Self
from .types import Vec3Like

from .Quat import Quat
from .Vec3 import Vec3

# REF
# https://gabormakesgames.com/blog_transforms_transforms.html
# https://gabormakesgames.com/blog_transforms_transform_world.html


class Transform:

    # region MAIN
    def __init__(self, t: Optional["Transform"] = None):
        if t:
            self.rot = t.rot.clone()
            self.pos = t.pos.clone()
            self.scl = t.scl.clone()
            return

        self.rot = Quat()
        self.pos = Vec3()
        self.scl = Vec3(1.0, 1.0, 1.0)

    # endregion

    # region SETTERS / GETTERS

    def copy(self, t: "Transform") -> Self:
        self.rot.copy(t.rot)
        self.pos.copy(t.pos)
        self.scl.copy(t.scl)
        return self

    def clone(self) -> "Transform":
        return Transform(self)

    # endregion

    # region OPERATORS

    # Computing Transforms, Parent -> Child
    def mul(self, tran: "Transform") -> Self:
        # vPOSITION - parent.position + ( parent.rotation * ( parent.scale * child.position ) )
        # This object is parent & input is child
        self.pos.add(Vec3().fromMul(self.scl, tran.pos).quatTransform(self.rot))

        # SCALE - parent.scale * child.scale
        self.scl.mul(tran.scl)

        # ROTATION - parent.rotation * child.rotation
        self.rot.mul(tran.rot)

        return self

    # Computing Transforms in reverse, Child - > Parent
    def pmul(self, tran: "Transform") -> Self:
        # POSITION - parent.position + ( parent.rotation * ( parent.scale * child.position ) )
        # This object is child and parent is input
        self.pos.mul(tran.scl).quatTransform(tran.rot).add(tran.pos)

        # SCALE - parent.scale * child.scale
        self.scl.mul(tran.scl)

        # ROTATION - parent.rotation * child.rotation
        self.rot.pmul(tran.rot)
        # Must Rotate from Parent->Child, need PMUL
        return self

    # endregion

    # region FROM OPERATORS

    def fromMul(self, tp: "Transform", tc: "Transform") -> Self:
        # POSITION - parent.position + (  ( parent.scale * child.position ) * parent.rotation )
        v = Vec3().fromMul(tp.scl, tc.pos).quatTransform(tp.rot)
        self.pos.fromAdd(tp.pos, v)

        # SCALE - parent.scale * child.scale
        self.scl.fromMul(tp.scl, tc.scl)

        # ROTATION - parent.rotation * child.rotation
        self.rot.fromMul(tp.rot, tc.rot)

        return self

    def fromInvert(self, t: "Transform") -> Self:
        # Invert Rotation
        self.rot.fromInvert(t.rot)

        # Invert Scale
        self.scl.fromInvert(t.scl)

        # Invert Position : rotInv * ( invScl * -Pos )
        self.pos.fromNegate(t.pos).mul(self.scl).quatTransform(self.rot)

        return self

    # endregion

    # region TRANSFORMATION

    def transformVec3(self, v: Vec3Like, out: Optional[Vec3]) -> Vec3:
        # GLSL - vecQuatRotation(model.rotation, a_position.xyz * model.scale) + model.position;
        out = out or Vec3()
        return out.fromMul(v, self.scl).quatTransform(self.rot).add(self.pos)

    # endregion
