import time
import math
import numpy as np
import pygfx as gfx
from rendercanvas.glfw import RenderCanvas  # Import RenderCanvas specifically for glfw
import pylinalg as la


class UseGfxDisplay:
    # region MAIN
    def __init__(self, _props={}):
        props = {"width": 800, "height": 600, "stats": True, "ortho": False, "zup": False, **_props}

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.onPreRender = None
        self.onPostRender = None
        self.isZup = props.get("zup")

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Core
        w = props.get("width")
        h = props.get("height")
        self.canvas = RenderCanvas(title=props.get("title", "Prototype Alpha Omega"), size=(w, h))
        self.renderer = gfx.WgpuRenderer(self.canvas)
        self.scene = gfx.Scene()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Camera
        if not props.get("ortho"):
            self.camera = gfx.PerspectiveCamera(45, w / h)
        else:
            self.camera = gfx.OrthographicCamera(w, h)

        if self.isZup:
            self.camera.world.reference_up = 0, 0, 1
            self.camera.local.position = (0, 7, 3)
        else:
            self.camera.local.position = (0, 3, 7)

        self.camCtrl = gfx.OrbitController(self.camera, register_events=self.renderer)
        self.camera.show_pos((0, 0, 0))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Timers
        self.lastFrameTime = time.perf_counter()
        self.startTime = self.lastFrameTime
        self.deltaTime = 0
        self.elapseTime = 0

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Finalize
        self.display = gfx.Display(
            canvas=self.canvas,
            renderer=self.renderer,
            camera=self.camera,
            controller=self.camCtrl,
        )

        self.display.stats = props.get("stats")
        self.display.before_render = self.preRender
        self.display.after_render = self.postRender

    def show(self):
        t = time.perf_counter()
        self.lastFrameTime = t
        self.startTime = t
        self.display.show(self.scene)

    # endregion

    # region METHODS
    # polar = [azimuth,zenith]
    def sphericalLook(self, polar, radius, target=(0, 0, 0)):

        if not self.isZup:
            # Y UP ROTATION
            azimuth = (polar[0] + 180) * math.pi / 180  # Horizontal plane
            zenith = (90 - polar[1]) * math.pi / 180  # Vertical plane

            self.camera.local.position = (
                -(radius * math.sin(zenith) * math.sin(azimuth)) + target[0],
                radius * math.cos(zenith) + target[1],
                -(radius * math.sin(zenith) * math.cos(azimuth)) + target[2],
            )
        else:
            # Z UP ROTATION
            azimuth = polar[0] * (math.pi / 180)
            zenith = polar[1] * (math.pi / 180)

            self.camera.local.position = (
                (radius * -math.sin(azimuth)) + target[0],
                radius * math.cos(azimuth) * math.cos(zenith) + target[1],
                (radius * math.cos(azimuth) * math.sin(zenith)) + target[2],
            )

        self.camera.show_pos(target)
        return self

    # endregion

    # region RENDER LOOP
    def preRender(self):
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Compute Times
        curTime = time.perf_counter()
        self.deltaTime = curTime - self.lastFrameTime
        self.elapseTime = curTime - self.startTime
        self.lastFrameTime = curTime

        # print(f"Delta time: {deltaTime:.6f} seconds")
        # print(f"Elapse time: {elapseTime:.6f} seconds")

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if self.onPreRender:
            self.onPreRender(self.deltaTime, self.elapseTime)

    def postRender(self):
        if self.onPostRender:
            self.onPostRender(self.deltaTime, self.elapseTime)

    # endregion

    # region EVENTS
    # https://jupyter-rfb.readthedocs.io/en/stable/events.html
    def on(self, evtName, evtFn):
        self.renderer.add_event_handler(evtFn, evtName)

    def off(self, evtName, evtFn):
        self.renderer.remove_event_handler(evtFn, evtName)

    # endregion


def useDarkScene(app):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Background
    bgColor = np.array((0.12, 0.12, 0.12, 1.0))
    app.scene.add(gfx.Background.from_color(bgColor))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Lighting
    app.scene.add(gfx.AmbientLight())
    # app.scene.add(gfx.DirectionalLight(intensity=0.8))
    dirLit = gfx.DirectionalLight(intensity=0.8)
    dirLit.local = (5, 10, 5)
    app.scene.add(dirLit)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Ground
    grid = gfx.GridHelper(
        size=20,
        divisions=20,
        thickness=1,
        color1=(0.25, 0.30, 0.25, 1),
        color2=(0.17, 0.17, 0.17, 1),
    )

    if app.isZup:
        grid.local.rotation = la.quat_from_euler([1.57079632679, 0, 0])

    app.scene.add(grid)

    return app
