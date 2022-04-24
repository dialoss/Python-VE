from src.utility.variables import *
import src.utility.geometry as geom
from src.utility.debug import *


class Mesh:
    def __init__(self, chunk, chunks):
        self.vBuffer = [0] * (W * H * D * 6 * 6 * V_SIZE)
        self.iBuffer = []
        self.chunk = chunk

        cx = chunk.posX
        cz = chunk.posZ
        nears = [None] * 4

        for i in range(4):
            c = geom.v[i]
            try:
                near = chunks[(cx + c[0]) * 100 + cz + c[1]]
                nears[i] = near
            except:
                continue

        self.nears = nears

        for x in range(W):
            for y in range(H):
                for z in range(D):
                    ind = chunk.voxels[z + D * (x + W * y)]
                    if ind == 0:
                        continue
                    for g in range(6):
                        self.add_side(g, x, y, z, ind)

    def check_nears(self, g, x, y, z):
        xn = x + geom.normals[g][0]
        yn = y + geom.normals[g][1]
        zn = z + geom.normals[g][2]
        if xn < 0 or zn < 0 or xn >= W or zn >= D:
            if self.nears[g] is not None:
                xn %= 16
                zn %= 16
                return self.nears[g].voxels[zn + D * (xn + W * yn)] != 0
            else:
                return False

        if yn < 0:
            return True

        return self.chunk.voxels[zn + D * (xn + W * yn)] != 0

    def add_side(self, g, x, y, z, ind):
        if self.check_nears(g, x, y, z):
            return
        v = geom.cube[g]
        pos = (z + D * (x + W * y)) * 6 * 6 * V_SIZE
        pos += g * 6 * V_SIZE
        for k in range(len(v)):
            self.vBuffer[pos] = v[k][0] + x
            self.vBuffer[pos + 1] = v[k][1] + y
            self.vBuffer[pos + 2] = v[k][2] + z
            self.vBuffer[pos + 3] = v[k][3]
            self.vBuffer[pos + 4] = v[k][4]
            self.vBuffer[pos + 5] = ind
            pos += 6

    def update_nears(self, x, y, z):
        for i in range(6):
            nx = x + geom.normals[i][0]
            ny = y + geom.normals[i][1]
            nz = z + geom.normals[i][2]
            self.add_side(geom.sides[i], nx, ny, nz, 1)

    def remove_block(self, x, y, z):
        pos = z + D * (x + W * y)
        pos *= 6 * 6 * V_SIZE
        for i in range(pos, pos + 6 * 6 * V_SIZE):
            self.vBuffer[i] = 0
        self.update_nears(x, y, z)

    def place_block(self, x, y, z, ind):
        for g in range(6):
            self.add_side(g, x, y, z, ind)
        self.update_nears(x, y, z)
