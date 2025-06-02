# region IMPORTS
from UseGfxDisplay import UseGfxDisplay, useDarkScene
from DynamicLines import DynamicLines
from Util import setTimeout

# endregion

# region SETUP
App = useDarkScene(UseGfxDisplay({"title": "Template Dynamic Lines"})).sphericalLook([0, 20], 10)

# def onPreRender(dt, et):
#     pass

# App.onPreRender = onPreRender
# endregion

# region MISC
dyLines = DynamicLines()
dyLines.add((0, 0, 0), (0, 1, 0), "#ff0000", "#00ff00")
dyLines.sync()
App.scene.add(dyLines)


def doSomething():
    dyLines.add([0, 1, 0], [1, 1, 0], "#00ff00").sync()


setTimeout(2, doSomething)
# endregion

# region RUN
App.show()
# endregion
