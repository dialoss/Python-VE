from queue import Queue
W = 16
H = 16
D = 16

V_SIZE = 3

coord_const = int(5e5)
buffer_size = 30000
upd_buffer_len = 0
free_places = Queue()
global_buffer = [0] * buffer_size * 36 * V_SIZE
updated_buffer = [0] * 2000 * 36 * V_SIZE
update_chunks = []
for i in range(buffer_size):
    free_places.put(i)


rx = 3
rz = 3
spawn_r = 3


# def resize_buffer():
#     global buffer_size
#     new_buf = [0] * buffer_size * 36 * V_SIZE
#     global_buffer.extend(new_buf)
#     for i in range(buffer_size, buffer_size * 2):
#         free_places.put(i)
#
#     buffer_size *= 2


def get_pos():
    global free_places
    if free_places.empty():
        # resize_buffer()
        pass

    return free_places.queue[0]


def add_to_buffer(vertices):
    global upd_buffer_len
    last = upd_buffer_len
    for i in range(last * 36 * V_SIZE, (last + 1) * 36 * V_SIZE):
        updated_buffer[i] = vertices[i - last * 36 * V_SIZE]

    upd_buffer_len += 1
    total_size = int(len(updated_buffer) / 36 / V_SIZE)
    if upd_buffer_len == total_size:
        new_buf = [0] * upd_buffer_len * 36 * V_SIZE
        updated_buffer.extend(new_buf)


def clear_updated_buffer():
    global upd_buffer_len
    upd_buffer_len = 0


def clear_global_buffer():
    global buffer_size
    buffer_size = 0
    global_buffer.clear()


def get_color(r, g, b):
    return r / 255, g / 255, b / 255
