from src.world.chunk import *


class ChunkManager:
    chunks = {}

    @classmethod
    def create(cls, width, depth):
        for i in range(width):
            for j in range(depth):
                cls.chunks[i * 100 + j] = Chunk(i, j)
        for i in range(width):
            for j in range(depth):
                chunk = cls.chunks[i * 100 + j]
                chunk.mesh = Mesh(chunk, cls.chunks)
                chunk.renderer = Renderer(chunk.mesh.vBuffer, chunk.mesh.iBuffer, [3, 2, 1])

    @classmethod
    def get_voxel(cls, x, y, z):
        if y < 0 or y >= H:
            return -1
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
    def get_chunk(cls, x, y, z):
        if y < 0 or y >= H:
            return -1
        cx = x // W
        cz = z // D
        try:
            chunk = cls.chunks[cx * 100 + cz]
            return chunk
        except:
            return None