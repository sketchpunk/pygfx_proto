# region IMPORTS
from UseGfxDisplay import gfx, UseGfxDisplay, useDarkScene
from Util import findFirst
import math

import pylinalg as la

from pathlib import Path

# endregion

# region SETUP
App = useDarkScene(UseGfxDisplay({"title": "Template GTLF Mesh & Skeleton"}))
App.sphericalLook([45, 20], 3, [0, 0.8, 0])

# Keep a copy of the bone's initial rotation
qthigh = None
qshin = None

# Path to resources
resPath = Path(__file__).parents[1] / "res"
print(f" Res - {resPath}")


def onPreRender(dt, et):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Animate Thigh
    n = (et) / 2
    n = n - math.floor(n)
    s = math.sin(math.pi * 2 * n)
    rad = s * (60 * (math.pi / 180))
    rot = la.quat_from_axis_angle([1, 0, 0], rad)
    skel.bones[44].local.rotation = la.quat_mul(qthigh, rot)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Animate Shin
    n = (et + 1) / 2  # Half cycle ahead
    n = n - math.floor(n)
    s = math.sin(math.pi * n)
    rad = s * (-80 * (math.pi / 180))
    rot = la.quat_from_axis_angle([1, 0, 0], rad)
    skel.bones[45].local.rotation = la.quat_mul(qshin, rot)


App.onPreRender = onPreRender
# endregion

# region MISC

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load GLTF model
glbPath = resPath / "nabba.glb"
gltf = gfx.load_gltf(glbPath, quiet=True)

# gfx.print_scene_graph(gltf.scene)

App.scene.add(gltf.scene)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Find the first skinned mesh loaded in
skel = None
mesh = findFirst(gltf.scene, lambda x: isinstance(x, gfx.objects.SkinnedMesh))
if mesh:
    print(f"Skinned Mesh {mesh.name}")

    # Add Skeleton renderer to scene
    skel = mesh.skeleton
    skelHelper = gfx.SkeletonHelper(skel.bones[0].parent)
    App.scene.add(skelHelper)

    # Save Copy of bone rotations for procedural animation
    qthigh = skel.bones[44].local.rotation.copy()
    qshin = skel.bones[45].local.rotation.copy()

    # See list of bones
    # for i, o in enumerate(mesh.skeleton.bones):
    #     print(f"{i} - {o.name}")

    # 44 - Thigh_L
    # 45 - Shin_L
    # 46 - Foot_L
# endregion

# region RUN
App.show()
# endregion
