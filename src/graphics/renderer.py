from pyglet.gl import *
import ctypes
from src.utility.variables import *


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
            ctypes.sizeof(GLfloat * len(vertices)),
            (GLfloat * len(vertices))(*vertices),
            GL_STATIC_DRAW
        )

        v_size = 0
        for i in attrs:
            v_size += i
        self.vCount = int(len(vertices) / v_size)

        shift = 0
        for i in range(len(attrs)):
            glVertexAttribPointer(i, attrs[i], GL_FLOAT, GL_FALSE, v_size * ctypes.sizeof(GLfloat), shift * ctypes.sizeof(GLfloat))
            glEnableVertexAttribArray(i)
            shift += attrs[i]

        self.ebo = GLuint(0)
        glGenBuffers(1, ctypes.byref(self.ebo))
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)

        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            ctypes.sizeof(GLuint * len(indices)),
            (GLuint * len(indices))(*indices),
            GL_STATIC_DRAW
        )

    def draw(self):
        glBindVertexArray(self.vao)
        # glDrawElements(GL_TRIANGLES, self.renderer.vCount, GL_UNSIGNED_INT, 0)
        glDrawArrays(GL_TRIANGLES, 0, self.vCount)