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
    return cnt <= 1


class Raycast:
    @classmethod
    def install(cls, world):
        cls.world = world

    @classmethod
    def hit_ray(cls, pos, dir, dist, normal):
        px = pos.x
        py = pos.y
        pz = pos.z

        sx = sign(dir.x)
        sy = sign(dir.y)
        sz = sign(dir.z)

        iter = 0

        while iter < dist:
            normal_tmp = [0, 0, 0]
            cx = math.floor(px)
            cy = math.floor(py)
            cz = math.floor(pz)

            type = cls.world.get_voxel(cx, cy, cz)
            if type >= 1:
                return [cx, cy, cz]
            if type == -1:
                return [1e9, 1e9, 1e9]

            dx = cx
            dy = cy
            dz = cz
            if sx > 0:
                dx += 1
            if sy > 0:
                dy += 1
            if sz > 0:
                dz += 1

            if abs(dir.x - 0) < 0.0000001:
                vx = 1e9
            else:
                vx = (dx - px) / dir.x
            if abs(dir.y - 0) < 0.0000001:
                vy = 1e9
            else:
                vy = (dy - py) / dir.y
            if abs(dir.z - 0) < 0.0000001:
                vz = 1e9
            else:
                vz = (dz - pz) / dir.z

            for i in range(3):
                if i == 0:
                    ny = dir.y * vx + py
                    nz = dir.z * vx + pz
                    if compare([cx, cy, cz], [dx, ny, nz]):
                        cx += sx
                        px = cx
                        py = ny
                        pz = nz
                        normal_tmp[0] = -sx
                        break
                if i == 1:
                    nx = dir.x * vy + px
                    nz = dir.z * vy + pz
                    if compare([cx, cy, cz], [nx, dy, nz]):
                        cy += sy
                        py = cy
                        px = nx
                        pz = nz
                        normal_tmp[1] = -sy
                        break
                if i == 2:
                    nx = dir.x * vz + px
                    ny = dir.y * vz + py
                    if compare([cx, cy, cz], [nx, ny, dz]):
                        cz += sz
                        pz = cz
                        py = ny
                        px = nx
                        normal_tmp[2] = -sz
                        break
            iter += 1
            normal[0] = normal_tmp[0]
            normal[1] = normal_tmp[1]
            normal[2] = normal_tmp[2]
        return [1e9, 1e9, 1e9]
