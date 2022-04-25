from src.world.chunk import *


class ChunkManager:
    chunks = {}
    global_mesh = []

    def __init__(self, width, depth):
        for i in range(-width, width + 1):
            for j in range(-depth, depth + 1):
                self.chunks[i * 100 + j] = Chunk(i, j)
        for i in range(-width, width + 1):
            for j in range(-depth, depth + 1):
                chunk = self.chunks[i * 100 + j]
                for k in range(4):
                    c = geom.v[k]
                    nx = i + c[0]
                    nz = j + c[1]
                    try:
                        chunk.nears[k] = self.chunks[nx * 100 + nz]
                    except:
                        continue
                chunk.mesh = Mesh(chunk)

    def get_voxel(self, x, y, z):
        if y < 0 or y >= H:
            return -1
        cx = x // W
        cz = z // D
        vx = x - cx * W
        vz = z - cz * D
        chunk = None
        try:
            chunk = self.chunks[cx * 100 + cz]
        except:
            return -1
        return chunk.voxels[vz + D * (vx + W * y)]

    def get_chunk(self, x, y, z):
        if y < 0 or y >= H:
            return None
        cx = x // W
        cz = z // D
        try:
            chunk = self.chunks[cx * 100 + cz]
            return chunk
        except:
            return None