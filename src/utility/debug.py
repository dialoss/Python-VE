import sys
from src.utility.variables import *


def log(*args):
    if len(args) == 1:
        if isinstance(args[0], list):
            print(args[0][0], args[0][1], args[0][2])
        else:
            print(args[0].x, args[0].y, args[0].z)
    else:
        print(*args)


def memory_usage(world):
    buf = sys.getsizeof(global_buffer)
    places = sys.getsizeof(free_places)
    print(buf, "global_buffer")
    print(places, "free_places")
    sz = 0
    for coord, chunk in world.chunks.items():
        sz += sys.getsizeof(chunk.voxels)
        sz += sys.getsizeof(chunk.posititons)
        sz += sys.getsizeof(chunk.mesh)
        sz += sys.getsizeof(chunk.numberSides)
    print(sz, "chunks")
    total = buf + sz + places
    total /= 1024 * 1024
    print(total, "total")
