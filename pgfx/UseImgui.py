from wgpu.utils.imgui import ImguiRenderer
from imgui_bundle import imgui


class UseImgui:
    # region MAIN
    def __init__(self, App, _props={}):
        props = {"width": 200, **_props}

        self.renderer = ImguiRenderer(App.renderer.device, App.canvas)
        self.renderer.set_gui(self._draw)
        self.width = props.get("width")
        self.onDraw = None

    # endregion

    # region RENDERING

    # Call doing a post render event to draw UI over the scene
    def render(self):
        self.renderer.render()

    def _draw(
        self,
    ):
        imgui.new_frame()
        imgui.set_next_window_size((self.width, 0), imgui.Cond_.always)
        imgui.set_next_window_pos(
            (self.renderer.backend.io.display_size.x - self.width, 0), imgui.Cond_.always
        )

        if self.onDraw:
            self.onDraw()

        imgui.end_frame()
        imgui.render()
        return imgui.get_draw_data()

    # endregion


# region UI ABSTTRACTION


# Create a button that will run a callback on click
def guiButton(title, fn):
    if imgui.button(title, size=(-1, 0)):
        fn()


# Create a Fload slider that has stepping applied to value
def guiFStepSlider(lbl, val, min=0, max=10, step=0.1, rndBy=1):
    changed, valOut = imgui.slider_float(
        lbl,
        val,
        min,
        max,
        "%.1f",  # Display format
    )

    # user has changed the value, apply stepping
    if changed:
        valOut = round(valOut / step, rndBy) * step

    return valOut


# endregion
