# region IMPORTS
from lib.UseGfxDisplay import UseGfxDisplay, useDarkScene
from lib.models.DynamicPoints import DynamicPoints
from lib.Util import setTimeout

# endregion

# region SETUP
App = useDarkScene(UseGfxDisplay({"title": "Template Dynamic Points"})).sphericalLook([0, 20], 10)

# def onPreRender(dt, et):
#     pass

# App.onPreRender = onPreRender
# endregion

# region MISC
dyPoints = DynamicPoints()
dyPoints.add((0, 1, 0), "#00ff00", 0.2)
dyPoints.sync()
App.scene.add(dyPoints)


def doSomething():
    dyPoints.add((-1, 0.5, 0), "#ff0000", 0.4).add((1, 1.5, 0), "#0000ff", 0.6).sync()


setTimeout(2, doSomething)
# endregion

# region RUN
App.show()
# endregion
