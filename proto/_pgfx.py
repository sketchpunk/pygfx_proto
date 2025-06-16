# region IMPORTS
from pgfx.UseGfxDisplay import UseGfxDisplay, useDarkScene
from pgfx.FacedCube import facedCube
import math

# endregion

# region SETUP
App = useDarkScene(UseGfxDisplay({"title": "Template Basic"})).sphericalLook([0, 20], 10)


def onPreRender(dt, et):
    cube.local.x = math.sin(et / 0.5) * 3


App.onPreRender = onPreRender
# endregion

# region MISC
cube = facedCube()
App.scene.add(cube)
# endregion

# region RUN
App.show()
# endregion
