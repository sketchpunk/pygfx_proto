# region IMPORTS
from lib.UseGfxDisplay import UseGfxDisplay, useDarkScene
from lib.UseVisDebug import UseVisDebug
import math
import pylinalg as la
import numpy as np

# endregion

# region SETUP
App = useDarkScene(UseGfxDisplay({"title": "Template Visual Debugging"}))
App.sphericalLook([45, 20], 5, [0, 0.8, 0])
Debug = UseVisDebug(App)


def onPreRender(dt, et):
    Debug.reset()
    calcLeg(et, 0, 2, -0.2)
    calcLeg(et, 1, 2, 0.2)
    Debug.sync()


def calcLeg(et, offset=0, m=2, x=0):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    thigh = np.float32([x, 2, 0])
    s = sin360(fract((et + offset) / m))
    q = la.quat_from_axis_angle([1, 0, 0], toRad(60) * s)
    toKnee = la.vec_transform_quat([0, -1, 0], q)
    knee = thigh + toKnee
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    s = sin180(fract((et + offset + (m / 0.5)) / m))
    q = la.quat_from_axis_angle([1, 0, 0], toRad(80) * s)
    toFoot = la.vec_transform_quat(toKnee, q)
    foot = knee + toFoot
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ps = 0.1
    ca = "#00ff00"
    cb = "#ff00ff"
    cc = "#00ffff"
    Debug.pnt.add(thigh, ca, ps).add(knee, cb, ps).add(foot, cc, ps)
    Debug.ln.add(thigh, knee, ca, cb).add(knee, foot, cb, cc)


App.onPreRender = onPreRender
# endregion


# region MATHS


def toRad(v):
    return v * (math.pi / 180)


def fract(v):
    return v - math.floor(v)


def sin360(n):
    return math.sin(math.pi * 2 * n)


def sin180(n):
    return math.sin(math.pi * n)


# endregion


# region RUN
App.show()
# endregion
