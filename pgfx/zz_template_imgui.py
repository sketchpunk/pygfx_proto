# region IMPORTS
from UseGfxDisplay import UseGfxDisplay, useDarkScene, testCube

from UseImgui import UseImgui, guiButton, guiFStepSlider
from imgui_bundle import imgui  # lots of warnings about GLFW being used twice?
import math

# endregion

# region SETUP
App = useDarkScene(UseGfxDisplay({"title": "Template Imgui"})).sphericalLook([0, 20], 10)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Render Events
def onPreRender(dt, et):
    cube.local.x = math.sin(et / 0.5) * 3


App.onPreRender = onPreRender


def onPostRender(dt, et):
    gui.render()


App.onPostRender = onPostRender
# endregion

# region BUILD UI
# Some UI elements will need some "state"
# as it does not hold any state internally
guiState = {
    "slider1": 0.0,
}


# A callback to generate the UI
def drawUI():
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # MAIN CONTAINER
    is_expand, _ = imgui.begin(
        "Controls",
        None,
        flags=imgui.WindowFlags_.no_move | imgui.WindowFlags_.no_resize,
    )

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ADD UI
    guiButton("Button 1", lambda: print("Button 1!!!"))

    guiButton("Button 2", lambda: print("Button 2!!!"))

    guiState["slider1"] = guiFStepSlider("Slider1", guiState["slider1"])

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # CLOSE MAIN CONTAINER
    imgui.end()


# Setup IMGUI
gui = UseImgui(App)
gui.onDraw = drawUI
# endregion

# region MISC
cube = testCube()
App.scene.add(cube)
# endregion

# region RUN
App.show()
# endregion
