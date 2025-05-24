# region IMPORTS
from UseGfxDisplay import UseGfxDisplay, useDarkScene, testCube
import math

# endregion

# region SETUP
App = useDarkScene(UseGfxDisplay({"title": "Template Basic"})).sphericalLook([0, 20], 10)


def onPreRender(dt, et):
    cube.local.x = math.sin(et / 0.5) * 3


App.onPreRender = onPreRender
# endregion

# region MISC
cube = testCube()
App.scene.add(cube)
# endregion

# region RUN
App.show()
# endregion
