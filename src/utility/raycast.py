import glm
from src.utility.variables import *
import math


def sign(val):
    if val < 0:
        return -1
    return 1


def compare(prev, cur):
    cnt = 0
    for i in range(3):
        if prev[i] != int(cur[i]):
            cnt += 1
    return cnt == 1


class Raycast:
    chunks = None
    @classmethod
    def set(cls, chunks):
        cls.chunks = chunks

    @classmethod
    def get_voxel(cls, x, y, z):
        cx = x // W
        cz = z // D
        vx = x - cx * W
        vz = z - cz * D
        chunk = None
        try:
            chunk = cls.chunks[cx * 100 + cz]
        except:
            return -1
        return chunk.voxels[vz + D * (vx + W * y)]

    @classmethod
    def hit_ray(cls, pos, dir, dist):
        sx = sign(dir.x)
        sy = sign(dir.y)
        sz = sign(dir.z)

        cx = math.floor(pos.x)
        cy = math.floor(pos.y)
        cz = math.floor(pos.z)

        iter = 0

        while iter < dist:
            type = cls.get_voxel(cx, cy, cz)
            if type >= 1:
                return [cx, cy, cz]
            if type == -1:
                return [1e9, 1e9, 1e9]

            dx = cx + sx
            dy = cy + sy
            dz = cz + sz

            if abs(dir.x - 0) < 0.0001:
                vx = (dx - pos.x)
            else:
                vx = (dx - pos.x) / dir.x
            if abs(dir.y - 0) < 0.0001:
                vy = (dy - pos.y)
            else:
                vy = (dy - pos.y) / dir.y
            if abs(dir.z - 0) < 0.0001:
                vz = (dz - pos.z)
            else:
                vz = (dz - pos.z) / dir.z

            for i in range(3):
                if i == 0:
                    ny = dir.y * vx + pos.y
                    nz = dir.z * vx + pos.z
                    if compare([cx, cy, cz], [dx, ny, nz]):
                        cx += sx
                        cy = int(ny)
                        cz = int(nz)
                        break
                if i == 1:
                    nx = dir.x * vy + pos.x
                    nz = dir.z * vy + pos.z
                    if compare([cx, cy, cz], [nx, dy, nz]):
                        cy += sy
                        cx = int(nx)
                        cz = int(nz)
                        break
                if i == 2:
                    nx = dir.x * vz + pos.x
                    ny = dir.y * vz + pos.y
                    if compare([cx, cy, cz], [nx, ny, dz]):
                        cz += sz
                        cx = int(nx)
                        cy = int(ny)
                        break
            iter += 1
        return [1e9, 1e9, 1e9]
