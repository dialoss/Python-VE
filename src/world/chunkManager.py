from src.world.chunk import *


class ChunkManager:
    chunks = {}

    def __init__(self, width, depth):
        for i in range(width):
            for j in range(depth):
                self.chunks[i * 100 + j] = Chunk(i, j)
        for i in range(width):
            for j in range(depth):
                chunk = self.chunks[i * 100 + j]
                chunk.mesh = Mesh(chunk, self.chunks)
                chunk.renderer = Renderer(chunk.mesh.vBuffer, chunk.mesh.iBuffer, [3, 2, 1])

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
            return -1
        cx = x // W
        cz = z // D
        try:
            chunk = self.chunks[cx * 100 + cz]
            return chunk
        except:
            return None