# region IMPORTS
import numpy as np
from UseGfxDisplay import UseGfxDisplay, useDarkScene, testCube
from DynamicPoints import DynamicPoints
from Util import inspectObj, dirObj, varObj, printDict

# endregion

# region SETUP
App = useDarkScene(UseGfxDisplay({"title": "Template Picking"})).sphericalLook([0, 20], 10)
# endregion

# region MISC
cube = testCube()
App.scene.add(cube)

dyPoints = DynamicPoints()
dyPoints.add([2, 2, -1], "#ff00ff", 0.2)
dyPoints.add([-2, 1, 1], "#00ff00", 0.2)
dyPoints.add([-1, -1, 0], "#00ffff", 0.2)
dyPoints.add([1, 1, 0], "#ffff00", 0.2)
dyPoints.sync()
App.scene.add(dyPoints)
# endregion


# region RUN
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def onPointDown(e):
    pi = e.pick_info
    if not pi["world_object"]:
        return
    
    obj = pi["world_object"]
    match pi:
        case x if "vertex_index" in pi and isinstance(x["world_object"], DynamicPoints):
            idx = pi['vertex_index']
            print(f"DynamicPoint - Id:{obj.id}, Idx:{idx}, pos:{obj.posAt(idx)}")
        case _:
            fi = pi['face_index']
            fc = pi["face_coord"]
            subi = np.argmax(fc)
            vi = int(obj.geometry.indices.data[fi, subi])
            pos = obj.geometry.positions.data[vi]

            print(f"Some Object - Id:{obj.id}, pos:{pos}, FaceIdx:{fi}, FaceCoord:{fc}")

    # print("~~~~~~~~~~~~~~~~~~~")
    # printDict( pi )

App.on("pointer_down", onPointDown)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# def onPreRender(dt, et):
#     pass

# App.onPreRender = onPreRender

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
App.show()
# endregion
