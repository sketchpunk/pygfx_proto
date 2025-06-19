# region IMPORTS
import pygfx as gfx
import numpy as np

# endregion


class DynamicLines(gfx.Line):
    # region MAIN
    def __init__(self, initCap=20, useDepth=True):
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        mat = gfx.LineSegmentMaterial(
            thickness=1,
            color_mode="vertex",
            thickness_space="screen",
            depth_test=useDepth,
        )
        super().__init__(
            None, mat, visible=True, render_order=100, render_mask="auto", name="DynPoints"
        )

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._dyCapacity = initCap  # how many lines
        self._dyCount = 0
        self._dyModified = False

        self._datPos = np.zeros((initCap * 2, 3), dtype=np.float32)
        self._datCol = np.ones((initCap * 2, 4), dtype=np.float32)

        self._buildGeometry()

    # endregion

    # region METHODS
    def add(self, apos, bpos, acol="#00ff00", bcol=None):
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Expand the local buffers if there is a need
        if self._dyCount >= self._dyCapacity:
            self.expandAlloc()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Create new data
        i = self._dyCount * 2
        self._datPos[i][0] = apos[0]
        self._datPos[i][1] = apos[1]
        self._datPos[i][2] = apos[2]

        self._datPos[i + 1][0] = bpos[0]
        self._datPos[i + 1][1] = bpos[1]
        self._datPos[i + 1][2] = bpos[2]

        gCol = gfx.Color(acol)
        self._datCol[i][0] = gCol[0]
        self._datCol[i][1] = gCol[1]
        self._datCol[i][2] = gCol[2]

        if bcol:
            gCol = gfx.Color(bcol)

        self._datCol[i + 1][0] = gCol[0]
        self._datCol[i + 1][1] = gCol[1]
        self._datCol[i + 1][2] = gCol[2]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Object management
        self._dyModified = True
        self._dyCount += 1
        return self

    def reset(self):
        self._dyCount = 0
        self.geometry.positions.draw_range = 0, self._dyCount * 2
        return self

    def sync(self):
        if self._dyModified:
            atCap = self.geometry.positions.data.size / 6  # 6 floats per line

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
        oldCap = self._dyCapacity * 2  # 2 points per line
        self._dyCapacity += s
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # new buffers
        pos = np.zeros((self._dyCapacity * 2, 3), dtype=np.float32)
        col = np.ones((self._dyCapacity * 2, 4), dtype=np.float32)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # copy data
        pos[0:oldCap] = self._datPos
        col[0:oldCap] = self._datCol

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # swop in new buffer space
        self._datPos = pos
        self._datCol = col

        return self

    def _buildGeometry(self):
        # TODO : gfx doesn't have a direct way to clean up GPU resources
        # From what I understand is if the geo looses all references
        # GC will clean it up will also clear out the GPU resources with it.

        # Create new geometry out of np arrays
        geo = gfx.Geometry(positions=self._datPos, colors=self._datCol)
        geo.positions.draw_range = 0, self._dyCount * 2
        self.geometry = geo

    def _updateGeometry(self):
        geo = self.geometry

        # Copy data over to geometry
        geo.positions.set_data(self._datPos)
        geo.colors.set_data(self._datCol)

        # geo.positions.update_full()
        geo.positions.draw_range = 0, self._dyCount * 2

    # endregion
