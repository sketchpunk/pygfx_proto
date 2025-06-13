# region IMPORTS
from UseGfxDisplay import gfx, UseGfxDisplay, useDarkScene, testCube
from Util import inspectObj, dirObj, varObj, printDict

# endregion

# region SETUP
App = useDarkScene(UseGfxDisplay({"title": "Template Picking"})).sphericalLook([0, 20], 10)
gizmo = gfx.TransformGizmo()
gizmo.add_default_event_handlers(App.renderer, App.camera)

App.scene.add(gizmo)
# endregion

# region MISC
cube = testCube()
App.scene.add(cube)

gizmo.set_object(cube)
gizmo.toggle_mode("world")  # object
gizmo.screen_size = 150
# endregion


# region RUN
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# def onPreRender(dt, et):
#     pass

# App.onPreRender = onPreRender

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
App.show()
# endregion
