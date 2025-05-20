# region IMPORTS
from lib.UseGfxDisplay import gfx, UseGfxDisplay, useDarkScene
from lib.Util import findFirst, swopClipSkeleton

from pathlib import Path

# endregion

# region SETUP
App = useDarkScene(UseGfxDisplay({"title": "Template GTLF Mesh & Skeleton"}))
App.sphericalLook([45, 20], 5, [0, 0.8, 0])

# Path to resources
resPath = Path(__file__).parents[1] / "res"
print(f" Res - {resPath}")


def onPreRender(dt, et):
    mixer.update(dt)


App.onPreRender = onPreRender
# endregion

# region MISC

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load GLTF

glMesh = gfx.load_gltf(resPath / "kaykit_mannequin.glb", quiet=True)
glAnim = gfx.load_gltf(resPath / "kaykit_animations.glb", quiet=True)

# gfx.print_scene_graph(glAnim.scene)

# Get character's skeleton
skel = findFirst(glMesh.scene, lambda x: isinstance(x, gfx.objects.SkinnedMesh)).skeleton

App.scene.add(glMesh.scene)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup Animator

# List out all the animations
# for i, clip in enumerate(glAnim.animations):
#     print(f"{i} - {clip.name}")
# 90 - Walking_A

mixer = gfx.AnimationMixer()
mixer.add_event_handler(lambda x: print("LoopEvent"), "loop")

# Fix clip so it will animate on loaded character skeleton
clip = glAnim.animations[90]
swopClipSkeleton(clip, skel)

# Start animating character
action = mixer.clip_action(clip)
action.play()

# endregion

# region RUN
App.show()
# endregion
