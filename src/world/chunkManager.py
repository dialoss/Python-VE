from src.world.chunk import *
import src.utility.variables as util
import time


def create_chunks(pos, should_close, world):
    while not should_close:
        px = int(pos.x) // W
        pz = int(pos.z) // D
        for x in range(-rx, rx + 1):
            for z in range(-rz, rz + 1):
                if x * x + z * z <= spawn_r:
                    cx = px + x
                    cz = pz + z
                    if world.chunks.get(cx * 100 + cz) is None:
                        chunk = Chunk(cx, cz)
                        world.chunks[cx * 100 + cz] = chunk
                        world.get_nears(chunk, cx, cz)
                        print(cx, cz)
                        chunk.mesh = Mesh(chunk)
                        world.update_chunks.append(chunk)
        time.sleep(2)


class ChunkManager:
    chunks = {}
    global_mesh = []
    update_chunks = []

    def __init__(self, width, depth):
        for i in range(-width, width + 1):
            for j in range(-depth, depth + 1):
                self.chunks[i * 100 + j] = Chunk(i, j)
        for i in range(-width, width + 1):
            for j in range(-depth, depth + 1):
                chunk = self.chunks[i * 100 + j]
                self.get_nears(chunk, i, j)
                chunk.mesh = Mesh(chunk)
                update_chunks.append(chunk)

    def get_nears(self, chunk, cx, cz):
        for k in range(4):
            c = geom.v[k]
            nx = cx + c[0]
            nz = cz + c[1]
            try:
                chunk.nears[k] = self.chunks[nx * 100 + nz]
            except:
                continue

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