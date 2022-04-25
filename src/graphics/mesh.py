from src.utility.variables import *
import src.utility.geometry as geom
from src.utility.debug import *


class Mesh:
    def __init__(self, chunk):
        self.chunk = chunk
        self.cx = chunk.posX
        self.cz = chunk.posZ

        for x in range(W):
            for y in range(H):
                for z in range(D):
                    ind = chunk.voxels[z + D * (x + W * y)]
                    if ind == 0:
                        continue
                    for g in range(6):
                        self.add_side(self.chunk, True, g, x, y, z, ind)

    def check_nears(self, chunk, g, x, y, z):
        xn = x + geom.normals[g][0]
        yn = y + geom.normals[g][1]
        zn = z + geom.normals[g][2]
        if xn < 0 or zn < 0 or xn >= W or zn >= D:
            if chunk.nears[g] is not None:
                xn %= 16
                zn %= 16
                return chunk.nears[g].voxels[zn + D * (xn + W * yn)] != 0
            else:
                return False

        if yn < 0:
            return True

        return self.chunk.voxels[zn + D * (xn + W * yn)] != 0

    def add_side(self, chunk, new_chunk, g, x, y, z, ind):
        if self.check_nears(chunk, g, x, y, z):
            return
        free_pos = chunk.posititons[z + D * (x + W * y)]
        if free_pos == -1:
            free_pos = get_pos()
            free_places.get(0)
            chunk.posititons[z + D * (x + W * y)] = free_pos
        v = geom.cube[g]

        chunk.numberSides[z + D * (x + W * y)] += 1

        buffer_pos = free_pos * 6 * 6 * V_SIZE
        buffer_pos += g * 6 * V_SIZE
        for k in range(len(v)):
            global_buffer[buffer_pos] = v[k][0] + x + chunk.posX * W
            global_buffer[buffer_pos + 1] = v[k][1] + y
            global_buffer[buffer_pos + 2] = v[k][2] + z + chunk.posZ * D
            global_buffer[buffer_pos + 3] = v[k][3]
            global_buffer[buffer_pos + 4] = v[k][4]
            global_buffer[buffer_pos + 5] = ind
            buffer_pos += 6

        if not new_chunk and not free_pos in to_update:
            to_update.append(free_pos)

    def remove_side(self, chunk, g, x, y, z):
        pos = chunk.posititons[z + D * (x + W * y)]
        if pos == -1:
            return

        chunk.numberSides[z + D * (x + W * y)] -= 1
        if chunk.numberSides[z + D * (x + W * y)] == 0:
            if not pos in to_update:
                to_update.append(pos)
                free_places.put(pos)
                chunk.posititons[z + D * (x + W * y)] = -1

        buffer_pos = pos * 6 * 6 * V_SIZE
        buffer_pos += g * 6 * V_SIZE
        for i in range(36):
            global_buffer[buffer_pos + i] = 0
        if not pos in to_update:
            to_update.append(pos)

    def update_nears(self, x, y, z):
        mid = self.chunk.voxels[z + D * (x + W * y)]
        for i in range(6):
            chunk = self.chunk
            nx = x + geom.normals[i][0]
            ny = y + geom.normals[i][1]
            nz = z + geom.normals[i][2]
            if nx < 0 or nz < 0 or nx >= W or nz >= D:
                chunk = self.chunk.nears[i]
                nx %= 16
                nz %= 16
            if chunk is None:
                continue
            ind = chunk.voxels[nz + D * (nx + W * ny)]
            if ind != 0:
                if mid == 0:
                    self.add_side(chunk, False, geom.sides[i], nx, ny, nz, ind)
                else:
                    self.remove_side(chunk, geom.sides[i], nx, ny, nz)

    def remove_block(self, x, y, z):
        pos = self.chunk.posititons[z + D * (x + W * y)]
        if pos == -1:
            return
        buffer_pos = pos * 6 * 6 * V_SIZE
        for i in range(buffer_pos, buffer_pos + 6 * 6 * V_SIZE):
            global_buffer[i] = 0
        to_update.append(pos)
        free_places.put(pos)
        self.chunk.posititons[z + D * (x + W * y)] = -1
        self.chunk.numberSides[z + D * (x + W * y)] = 0
        self.update_nears(x, y, z)

    def place_block(self, x, y, z):
        ind = self.chunk.voxels[z + D * (x + W * y)]
        for g in range(6):
            self.add_side(self.chunk, False, g, x, y, z, ind)
        self.update_nears(x, y, z)
