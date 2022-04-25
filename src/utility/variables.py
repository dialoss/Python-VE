from queue import Queue
W = 16
H = 16
D = 16

V_SIZE = (3 + 2 + 1)

buffer_size = 10000
free_places = Queue()
global_buffer = [0] * buffer_size * 6 * 6 * V_SIZE
to_update = []
for i in range(10000):
    free_places.put(i)


def resize_buffer():
    global buffer_size
    for i in range(buffer_size, buffer_size * 2):
        free_places.put(i)
        for j in range(6 * 6 * V_SIZE):
            global_buffer.append(0)

    buffer_size *= 2


def get_pos():
    global free_places
    if free_places.empty():
        resize_buffer()

    return free_places.queue[0]


def get_color(r, g, b):
    return r / 255, g / 255, b / 255
