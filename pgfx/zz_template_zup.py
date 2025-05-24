# region IMPORTS
from UseGfxDisplay import gfx, UseGfxDisplay, useDarkScene

from UseVisDebug import UseVisDebug

# endregion

# region SETUP
App = useDarkScene(UseGfxDisplay({"title": "Template Zup", "zup": True}))
App.sphericalLook([45, 20], 10)
Debug = UseVisDebug(App)

# def onPreRender(dt, et):
#     pass

# App.onPreRender = onPreRender

# endregion

# region MISC
App.scene.add(gfx.AxesHelper())

Debug.pnt.add([1.5, 0, 0], "#ff0000", 0.2)
Debug.pnt.add([0, 1.5, 0], "#00ff00", 0.2)
Debug.pnt.add([0, 0, 1.5], "#0000ff", 0.2)
Debug.sync()
# endregion

# region RUN
App.show()
# endregion
