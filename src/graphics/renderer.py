from pyglet.gl import *
import ctypes
from src.utility.variables import *
from collections import deque


class LineRenderer:
    def __init__(self, vertices, attrs):
        self.vao = GLuint(0)
        glGenVertexArrays(1, ctypes.byref(self.vao))
        glBindVertexArray(self.vao)

        self.vbo = GLuint(0)
        glGenBuffers(1, ctypes.byref(self.vbo))
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        glBufferData(
            GL_ARRAY_BUFFER,
            ctypes.sizeof(GLfloat * len(vertices)),
            (GLfloat * len(vertices))(*vertices),
            GL_STATIC_DRAW
        )

        v_size = 0
        for i in attrs:
            v_size += i
        self.vCount = len(vertices) // v_size

        shift = 0
        for i in range(len(attrs)):
            glVertexAttribPointer(i, attrs[i], GL_FLOAT, GL_FALSE, v_size * ctypes.sizeof(GLfloat),
                                   shift * ctypes.sizeof(GLfloat))
            glEnableVertexAttribArray(i)
            shift += attrs[i]

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.vCount)


class Renderer:
    def __init__(self, vertices, indices, attrs):
        self.vao = GLuint(0)
        glGenVertexArrays(1, ctypes.byref(self.vao))
        glBindVertexArray(self.vao)

        self.vbo = GLuint(0)
        glGenBuffers(1, ctypes.byref(self.vbo))
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        glBufferData(
            GL_ARRAY_BUFFER,
            ctypes.sizeof(GLuint * len(vertices)),
            (GLuint * len(vertices))(*vertices),
            GL_STATIC_DRAW
        )

        v_size = 0
        for i in attrs:
            v_size += i
        self.vCount = len(vertices) // v_size

        shift = 0
        for i in range(len(attrs)):
            glVertexAttribIPointer(i, attrs[i], GL_UNSIGNED_INT, v_size * ctypes.sizeof(GLuint),
                                  shift * ctypes.sizeof(GLuint))
            glEnableVertexAttribArray(i)
            shift += attrs[i]

        # self.ebo = GLuint(0)
        # glGenBuffers(1, ctypes.byref(self.ebo))
        # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        #
        # glBufferData(
        #     GL_ELEMENT_ARRAY_BUFFER,
        #     ctypes.sizeof(GLuint * len(indices)),
        #     (GLuint * len(indices))(*indices),
        #     GL_STATIC_DRAW
        # )

    def update(self, chunk):
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        vertices = chunk.buffer
        to_update = chunk.to_update

        count = 0
        for pos, sides in to_update.items():
            for side in sides:
                buffer_pos = pos * 36 * V_SIZE + side * 6 * V_SIZE
                data = [0] * 6 * V_SIZE
                for i in range(side * 6 * V_SIZE, (side + 1) * 6 * V_SIZE):
                    data[i - side * 6 * V_SIZE] = vertices[count * 36 * V_SIZE + i]
                    vertices[count * 36 * V_SIZE + i] = 0

                glBufferSubData(
                    GL_ARRAY_BUFFER,
                    ctypes.sizeof(GLuint * buffer_pos),
                    ctypes.sizeof(GLuint * len(data)),
                    (GLuint * len(data))(*data)
                )
            count += 1

    def draw(self):
        glBindVertexArray(self.vao)
        # glDrawElements(GL_TRIANGLES, self.renderer.vCount, GL_UNSIGNED_INT, 0)
        glDrawArrays(GL_TRIANGLES, 0, self.vCount)