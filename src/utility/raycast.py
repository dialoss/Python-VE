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
                vx = abs((dx - px) / dir.x)
            if abs(dir.y - 0) < 0.0000001:
                vy = 1e9
            else:
                vy = abs((dy - py) / dir.y)
            if abs(dir.z - 0) < 0.0000001:
                vz = 1e9
            else:
                vz = abs((dz - pz) / dir.z)

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

    @classmethod
    def hit_ray_new(cls, pos, dir, dist, normal):
        px = pos.x
        py = pos.y
        pz = pos.z

        dx = dir.x
        dy = dir.y
        dz = dir.z

        t = 0
        ix = math.floor(px)
        iy = math.floor(py)
        iz = math.floor(pz)

        stepx = sign(dx)
        stepy = sign(dy)
        stepz = sign(dz)

        inf = 1e15

        txDelta = inf
        tyDelta = inf
        tzDelta = inf

        if dx != 0:
            txDelta = abs(1 / dx)
        if dy != 0:
            tyDelta = abs(1 / dy)
        if dz != 0:
            tzDelta = abs(1 / dz)

        xdist = ix + 1 - px
        ydist = iy + 1 - py
        zdist = iz + 1 - pz

        if stepx <= 0:
            xdist = px - ix
        if stepy <= 0:
            ydist = py - iy
        if stepz <= 0:
            zdist = pz - iz

        txMax = inf
        tyMax = inf
        tzMax = inf

        if txDelta < inf:
            txMax = txDelta * xdist
        if tyDelta < inf:
            tyMax = tyDelta * ydist
        if tzDelta < inf:
            tzMax = tzDelta * zdist

        steppedIndex = -1

        while t <= dist:
            type = cls.world.get_voxel(ix, iy, iz)
            if type >= 1:
                if steppedIndex == 0:
                    normal[0] = -stepx
                if steppedIndex == 1:
                    normal[1] = -stepy
                if steppedIndex == 2:
                    normal[2] = -stepz
                return [ix, iy, iz]
            if type == -1:
                return [1e9, 1e9, 1e9]

            if txMax < tyMax:
                if txMax < tzMax:
                    ix += stepx
                    t = txMax
                    txMax += txDelta
                    steppedIndex = 0

                else:
                    iz += stepz
                    t = tzMax
                    tzMax += tzDelta
                    steppedIndex = 2
            else:
                if tyMax < tzMax:
                    iy += stepy
                    t = tyMax
                    tyMax += tyDelta
                    steppedIndex = 1
                else:
                    iz += stepz
                    t = tzMax
                    tzMax += tzDelta
                    steppedIndex = 2

        return [1e9, 1e9, 1e9]