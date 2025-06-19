from pgfx.DynamicLines import DynamicLines
from pgfx.DynamicPoints import DynamicPoints


class UseVisDebug:

    def __init__(self, App, _props={}):
        props = {"pntSize": 20, "lnSize": 20, "useDepth": True, **_props}

        self.pnt = DynamicPoints(props["pntSize"], props["useDepth"])
        self.ln = DynamicLines(props["lnSize"], props["useDepth"])
        App.scene.add(self.pnt)
        App.scene.add(self.ln)

    def reset(self):
        self.pnt.reset()
        self.ln.reset()

    def sync(self):
        self.pnt.sync()
        self.ln.sync()
