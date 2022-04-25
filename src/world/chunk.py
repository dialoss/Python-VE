from src.utility.variables import *
from src.graphics.mesh import *
from src.graphics.renderer import *
import math


class Chunk:
    def __init__(self, posX, posZ):
        self.mesh = None
        self.voxels = [0] * W * H * D
        self.posititons = [-1] * W * H * D
        self.numberSides = [0] * W * H * D
        self.nears = [None] * 4
        self.posX = posX
        self.posZ = posZ
        for x in range(W):
            for z in range(D):
                realX = W * posX + x
                realZ = D * posZ + z
                h = max(int(math.sin(realX * 0.5) * 10), 5)
                for y in range(h):
                    if y < 4:
                        self.voxels[z + D * (x + W * y)] = 2
                    else:
                        self.voxels[z + D * (x + W * y)] = 1
