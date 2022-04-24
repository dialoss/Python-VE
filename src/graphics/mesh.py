from src.utility.variables import *
import src.utility.geometry as geom
from src.utility.debug import *


def check_nears(ind, chunk, nears, x, y, z):
    xn = x + geom.normals[ind][0]
    yn = y + geom.normals[ind][1]
    zn = z + geom.normals[ind][2]
    if xn < 0 or zn < 0 or xn >= W or zn >= D:
        if nears[ind] is not None:
            xn %= 16
            zn %= 16
            return nears[ind].voxels[zn + D * (xn + W * yn)] != 0
        return True

    if yn < 0:
        return True

    return chunk.voxels[zn + D * (xn + W * yn)] != 0


class Mesh:
    def __init__(self, chunk, chunks):
        self.iBuffer = []
        self.vBuffer = []

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

        for x in range(W):
            for y in range(H):
                for z in range(D):
                    ind = chunk.voxels[z + D * (x + W * y)]
                    if ind == 0:
                        continue
                    for g in range(6):
                        if check_nears(g, chunk, nears, x, y, z):
                            continue
                        v = geom.cube[g]
                        # ind = geom.indices[g]
                        # for k in range(len(ind)):
                        #     self.iBuffer.append(ind[k] + z + D * (x + W * y))
                        for k in range(len(v)):
                            self.vBuffer.append(v[k][0] + x)
                            self.vBuffer.append(v[k][1] + y)
                            self.vBuffer.append(v[k][2] + z)
                            self.vBuffer.append(v[k][3])
                            self.vBuffer.append(v[k][4])
                            self.vBuffer.append(ind)