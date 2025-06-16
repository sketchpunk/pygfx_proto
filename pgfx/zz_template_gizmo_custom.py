# region IMPORTS
from UseGfxDisplay import gfx, UseGfxDisplay, useDarkScene
from Util import inspectObj, dirObj, varObj, printDict
from FacedCube import facedCube
from UseGizmo import useGizmo

# endregion

# region SETUP
App = useDarkScene(UseGfxDisplay({"title": "Template Picking"})).sphericalLook([0, 20], 10)
gizmo = useGizmo(App)
# endregion

# region MISC
cube = facedCube()
App.scene.add(cube)

gizmo.set_object(cube)

# endregion


# region RUN


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def onGizmoMove(v):
    print(f"GizmoMove: {v}")


def onGizmoRotate(v):
    print(f"GizmoRotate: {v}")


def onGizmoScale(v):
    print(f"GizmoScale: {v}")


def onGizmoDragStart():
    print("Gizmo Drag Start")


def onGizmoDragEnd():
    print("Gizmo Drag End")


gizmo.onMove = onGizmoMove
gizmo.onRotate = onGizmoRotate
gizmo.onScale = onGizmoScale
gizmo.onDragStart = onGizmoDragStart
gizmo.onDragEnd = onGizmoDragEnd

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# def onPreRender(dt, et):
#     pass

# App.onPreRender = onPreRender

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
App.show()
# endregion
