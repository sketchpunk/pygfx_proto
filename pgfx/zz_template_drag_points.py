# region IMPORTS
from UseGfxDisplay import gfx, UseGfxDisplay, useDarkScene
from DynamicPoints import DynamicPoints
# from Util import inspectObj, dirObj, varObj, printDict
from UseGizmo import useGizmo

# endregion

# region SETUP
App = useDarkScene(UseGfxDisplay({"title": "Template Drag Points"})).sphericalLook([0, 20], 10)

gizmo = useGizmo(App)
gizObject = gfx.WorldObject()
gizObject.local.position = [0,1,0]
gizmo.set_object( gizObject )
gizmo.toggle_mode("world") # Remove scale controls

dyPoints = DynamicPoints()
App.scene.add(dyPoints)

# endregion

# region PROTO

# Need an object to store a single value else
# there is no way to mutate the value when using
# a global int value
state = {
    "sel": -1
}

points = [
    {"v": [-1, 1, 0], "c": "#00ff00"},
    {"v": [1, 1, 0], "c": "#ff0000"},
]

def redrawPoints():
    dyPoints.reset()
    pntSize = 0.2

    for p in points:
        dyPoints.add(p["v"], p["c"], pntSize)
        print( p["v"] )

    dyPoints.sync()

redrawPoints()

# endregion

# region RUN
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Mouse Events
def onPicking(e):
    pi = e.pick_info
    if not pi["world_object"]:
        return

    obj = pi["world_object"]
    match pi:
        case x if "vertex_index" in pi and isinstance(x["world_object"], DynamicPoints):
            sel = state["sel"] = pi['vertex_index']
            gizmo.set_object( gizObject )
            gizObject.local.position = points[ sel ]["v"]
            print(f"DynamicPoint - Id:{obj.id}, Idx:{sel}, pos:{obj.posAt(sel)}")

App.on("pointer_down", onPicking)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Keyboard Events
def onKeyDown(e):
    # print("KeyDown", e.key)
    if e.key == " ":
        state["sel"] = -1
        gizmo.set_object( None )

App.on("key_down", onKeyDown)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Gizmo Events
def onGizmoMove(v):
    # print(f"GizmoMove: {v}")
    sel = state["sel"]
    if sel != -1:
        points[ sel ]["v"] = v

def onGizmoDragEnd():
    # print("GizmoDragEnd")
    redrawPoints()

gizmo.onMove = onGizmoMove
gizmo.onDragEnd = onGizmoDragEnd

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Render Loop
# def onPreRender(dt, et):
#     pass

# App.onPreRender = onPreRender

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
App.show()
# endregion
