from src.utility.variables import *
import src.utility.geometry as geom
from src.utility.debug import *


def set_rgb(r, g, b, v):
    v |= (r << 28)
    v |= (g << 24)
    v |= (b << 20)
    return v


def set_texture(tx, ty, ind, v):
    v |= (tx << 31)
    v |= (ty << 30)
    v |= (ind << 20)
    return v


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
                        self.add_side(self.chunk, g, x, y, z, ind)
                    if chunk.posititons[z + D * (x + W * y)] != -1:
                        chunk.count += 1

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

    def add_to_buffer(self):
        # new_buf = [0] * buffer_size * 36 * V_SIZE
        # global_buffer.extend(new_buf)
        # for i in range(buffer_size, buffer_size * 2):
        #     free_places.put(i)
        #
        # buffer_size *= 2
        pass

    def add_side(self, chunk, g, x, y, z, ind):
        if self.check_nears(chunk, g, x, y, z):
            return
        free_pos = chunk.posititons[z + D * (x + W * y)]
        if free_pos == -1:
            free_pos = get_pos()
            free_places.get(0)
            chunk.posititons[z + D * (x + W * y)] = free_pos
        v = geom.cube[g]

        chunk.numberSides[z + D * (x + W * y)] += 1

        buffer_pos = chunk.count * 36 * V_SIZE + g * 6 * V_SIZE
        for k in range(len(v)):
            vx = v[k][0] + x + chunk.posX * W + coord_const
            vy = v[k][1] + y + coord_const
            vy = set_rgb(0, 0, 0, vy)
            vz = v[k][2] + z + chunk.posZ * D + coord_const
            vz = set_texture(v[k][3], v[k][4], ind, vz)
            chunk.buffer[buffer_pos] = vx
            chunk.buffer[buffer_pos + 1] = vy
            chunk.buffer[buffer_pos + 2] = vz
            buffer_pos += V_SIZE

        if chunk.to_update.get(free_pos) is None:
            chunk.to_update[free_pos] = []
        chunk.to_update[free_pos].append(g)

    def remove_side(self, chunk, g, x, y, z):
        pos = chunk.posititons[z + D * (x + W * y)]
        if pos == -1:
            return

        chunk.numberSides[z + D * (x + W * y)] -= 1
        if chunk.numberSides[z + D * (x + W * y)] == 0:
            free_places.put(pos)
            chunk.posititons[z + D * (x + W * y)] = -1

        buffer_pos = chunk.mesh.count * 36 * V_SIZE + g * 6 * V_SIZE
        for i in range(6 * V_SIZE):
            chunk.mesh.buffer[buffer_pos + i] = 0

        if chunk.to_update.get(pos) is None:
            chunk.to_update[pos] = []
        chunk.to_update[pos].append(g)

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
                    self.add_side(chunk, geom.sides[i], nx, ny, nz, ind)
                else:
                    self.remove_side(chunk, geom.sides[i], nx, ny, nz)

    def remove_block(self, x, y, z):
        pos = self.chunk.posititons[z + D * (x + W * y)]
        if pos == -1:
            return

        for i in range(36 * V_SIZE):
            pass
        self.chunk.to_update[pos] = [0, 1, 2, 3, 4, 5]
        free_places.put(pos)
        self.chunk.posititons[z + D * (x + W * y)] = -1
        self.chunk.numberSides[z + D * (x + W * y)] = 0
        self.update_nears(x, y, z)

    def place_block(self, x, y, z):
        ind = self.chunk.voxels[z + D * (x + W * y)]
        for g in range(6):
            self.add_side(self.chunk, g, x, y, z, ind)
        update_chunks.append(self.chunk)
        self.update_nears(x, y, z)
