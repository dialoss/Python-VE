from src.utility.variables import *
from src.graphics.mesh import *
from src.graphics.renderer import *
import math


class Chunk:
    def __init__(self, posX, posZ):
        self.mesh = None
        self.to_update = dict()
        self.voxels = [0] * W * H * D
        self.posititons = [-1] * W * H * D
        self.numberSides = [0] * W * H * D
        self.count = 0
        self.buffer_size = 2000
        self.buffer = [0] * self.buffer_size * 36 * V_SIZE
        self.nears = [None] * 4
        self.posX = posX
        self.posZ = posZ
        for x in range(W):
            for z in range(D):
                realX = W * posX + x
                realZ = D * posZ + z
                h = max(int(math.sin(realX * 0.2) * 10), 5)
                for y in range(h):
                    if y < 4:
                        self.voxels[z + D * (x + W * y)] = 2
                    else:
                        self.voxels[z + D * (x + W * y)] = 1

    def clear_buffers(self):
        self.to_update.clear()
        self.buffer = [0] * 100 * 36 * V_SIZE