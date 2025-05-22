from lib.models.DynamicLines import DynamicLines
from lib.models.DynamicPoints import DynamicPoints


class UseVisDebug:
    def __init__(self, App):
        self.pnt = DynamicPoints()
        self.ln = DynamicLines()
        App.scene.add(self.pnt)
        App.scene.add(self.ln)

    def reset(self):
        self.pnt.reset()
        self.ln.reset()

    def sync(self):
        self.pnt.sync()
        self.ln.sync()
