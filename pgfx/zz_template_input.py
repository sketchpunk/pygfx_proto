# region IMPORTS
from UseGfxDisplay import UseGfxDisplay, useDarkScene
from FacedCube import facedCube
import math

# endregion

# region SETUP
App = useDarkScene(UseGfxDisplay({"title": "Template Input"})).sphericalLook([0, 20], 10)

doAnim = True


def onPreRender(dt, et):
    if doAnim:
        cube.local.x = math.sin(et / 0.5) * 3


App.onPreRender = onPreRender
# endregion


# region EVENTS
# https://jupyter-rfb.readthedocs.io/en/stable/events.html
def onKeyDown(e):
    global doAnim
    print("KeyDown", e.key)
    if e.key == " ":
        doAnim = not doAnim


App.on("key_down", onKeyDown)


def onPointerDown(e):
    global doAnim
    print("PointerDown", e.x, e.y, e.button, e.buttons, e.modifiers)
    if "Shift" in e.modifiers:
        doAnim = not doAnim


App.on("pointer_down", onPointerDown)


def onResize(e):
    print("Resize", e.width, e.height, e.pixel_ratio, e.time_stamp)


App.on("resize", onResize)
# endregion

# region MISC
cube = facedCube()
App.scene.add(cube)
# endregion

# region RUN
App.show()
# endregion
