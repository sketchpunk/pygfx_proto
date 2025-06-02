# region IMPORTS
import pygfx as gfx
import numpy as np

# TODO - Check out the shapes points material, see if it can be used dynamically with geometry
# # https://github.com/pygfx/pygfx/blob/fbbc0cdd3a72988d5927c7236f0a2f0f9d9e940d/pygfx/materials/_points.py#L340
# endregion


class DynamicPoints(gfx.Points):
    # region MAIN
    def __init__(self, initCap=20):
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        mat = gfx.PointsMaterial(color_mode="vertex", size_space="world", size_mode="vertex")
        super().__init__(
            None, mat, visible=True, render_order=101, render_mask="auto", name="DynPoints"
        )

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._dyCapacity = initCap
        self._dyCount = 0
        self._dyModified = False

        self._datPos = np.zeros((initCap, 3), dtype=np.float32)
        self._datCol = np.ones((initCap, 4), dtype=np.float32)
        self._datSiz = np.zeros(initCap, dtype=np.float32)

        self._buildGeometry()

    # endregion

    # region METHODS
    def add(self, pos, col="#00ff00", size=0.2):
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Expand the local buffers if there is a need
        if self._dyCount >= self._dyCapacity:
            self.expandAlloc()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Create new data
        i = self._dyCount
        self._datPos[i][0] = pos[0]
        self._datPos[i][1] = pos[1]
        self._datPos[i][2] = pos[2]

        gCol = gfx.Color(col)
        self._datCol[i][0] = gCol[0]
        self._datCol[i][1] = gCol[1]
        self._datCol[i][2] = gCol[2]

        self._datSiz[i] = size

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Object management
        self._dyModified = True
        self._dyCount += 1
        return self

    def reset(self):
        self._dyCount = 0
        self.geometry.positions.draw_range = 0, self._dyCount
        return self

    def sync(self):
        if self._dyModified:
            atCap = self.geometry.positions.data.size / 3

            if self._dyCapacity > atCap:
                # Need to geometry buffer to handle expanded data
                self._buildGeometry()
            else:
                # Data within range, update existing geometry
                self._updateGeometry()

            self._dyModified = False

        return self

    # endregion

    # region MANAGE GEOMETRY & DATA BUFFERS
    def expandAlloc(self, s=20):
        oldCap = self._dyCapacity
        self._dyCapacity += s
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # new buffers
        pos = np.zeros((self._dyCapacity, 3), dtype=np.float32)
        col = np.ones((self._dyCapacity, 4), dtype=np.float32)
        siz = np.zeros(self._dyCapacity, dtype=np.float32)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # copy data
        pos[0:oldCap] = self._datPos
        col[0:oldCap] = self._datCol
        siz[0:oldCap] = self._datSiz

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # swop in new buffer space
        self._datPos = pos
        self._datCol = col
        self._datSiz = siz

        return self

    def _buildGeometry(self):
        # TODO : gfx doesn't have a direct way to clean up GPU resources
        # From what I understand is if the geo looses all references
        # GC will clean it up will also clear out the GPU resources with it.
        # if self.geometry:
        # del self.geometry.positions
        # del self.geometry.colors
        # del self.geometry.sizes
        # del self.geometry
        # print("--DELETE OLD GEOMETRY")

        # Create new geometry out of np arrays
        geo = gfx.Geometry(positions=self._datPos, sizes=self._datSiz, colors=self._datCol)
        geo.positions.draw_range = 0, self._dyCount
        self.geometry = geo

    def _updateGeometry(self):
        geo = self.geometry

        # Copy data over to geometry
        geo.positions.set_data(self._datPos)
        geo.sizes.set_data(self._datSiz)
        geo.colors.set_data(self._datCol)

        # geo.positions.update_full()
        geo.positions.draw_range = 0, self._dyCount

    # endregion
