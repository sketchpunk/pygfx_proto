# region IMPORTS
from UseGfxDisplay import UseGfxDisplay, useDarkScene, gfx
from FacedCube import facedCube
from Util import inspectObj, dirObj, varObj, printDict

import math

# endregion

# region SETUP
App = useDarkScene(UseGfxDisplay({"title": "Template Basic"})).sphericalLook([0, 20], 10)
# endregion


# region MISC
cube = facedCube()
App.scene.add(cube)
# endregion


# region RUN
def onPreRender(dt, et):
    cube.local.x = math.sin(et / 0.5) * 3


App.onPreRender = onPreRender

App.show()
# endregion
