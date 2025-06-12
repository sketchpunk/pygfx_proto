# region IMPORTS

from pgfx.UseGfxDisplay import UseGfxDisplay, useDarkScene, testCube
import math

from maths import Maths

# endregion

# region SETUP
App = useDarkScene(UseGfxDisplay({"title": "Template Basic"})).sphericalLook([0, 20], 10)
# endregion

# region MISC
cube = testCube()
App.scene.add(cube)
# endregion


# region RUN
def onPreRender(dt, et):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    # Anomate Cube
    cube.local.x = math.sin(et / 0.5) * 3

    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    # Animate orbit camera
    t = Maths.fract(et / 10)  # Full rotation per X seconds
    lon = Maths.wrap(360 * t, -180, 180)
    App.sphericalLook([lon, 20], 10, [0, 0.0, 0])


App.onPreRender = onPreRender

App.show()
# endregion
