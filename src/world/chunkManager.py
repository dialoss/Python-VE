from src.world.chunk import *


class ChunkManager:
    def __init__(self, x, z):
        self.chunks = {}
        for i in range(x):
            for j in range(z):
                self.chunks[i * 100 + j] = Chunk(i, j)
        for i in range(x):
            for j in range(z):
                chunk = self.chunks[i * 100 + j]
                chunk.mesh = Mesh(chunk, self.chunks)
                chunk.renderer = Renderer(chunk.mesh.vBuffer, chunk.mesh.iBuffer, [3, 2, 1])