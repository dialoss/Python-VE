import ctypes
from pyglet.gl import *
from src.glmath import Matrix
import glm


def create_shader(target, path):
    source_f = open(path, "rb")
    source = source_f.read()
    source_f.close()

    length = ctypes.c_int(len(source) + 1)
    buffer = ctypes.create_string_buffer(source)
    buffer_pointer = ctypes.cast(
        ctypes.pointer(ctypes.pointer(buffer)),
        ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
    )

    glShaderSource(target, 1, buffer_pointer, ctypes.byref(length))
    glCompileShader(target)

    log = GLint(0)
    glGetShaderiv(target, GL_INFO_LOG_LENGTH, ctypes.byref(log))

    log_buffer = ctypes.create_string_buffer(log.value)
    glGetShaderInfoLog(target, log, None, log_buffer)

    if log:
        print(log_buffer.value)


class Shader:
    def __init__(self, vert_path, frag_path):
        self.program = glCreateProgram()

        self.vert_shader = glCreateShader(GL_VERTEX_SHADER)
        create_shader(self.vert_shader, vert_path)
        glAttachShader(self.program, self.vert_shader)

        self.frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        create_shader(self.frag_shader, frag_path)
        glAttachShader(self.program, self.frag_shader)

        glLinkProgram(self.program)

        glDeleteShader(self.vert_shader)
        glDeleteShader(self.frag_shader)

    def __del__(self):
        glDeleteProgram(self.program)

    def use(self):
        glUseProgram(self.program)

    def uniformv(self, name, value):
        pos = glGetUniformLocation(self.program, name.encode('ascii'))
        if len(value) == 4:
            glUniform4f(pos, *value)
        if len(value) == 3:
            glUniform3f(pos, *value)

    def uniformm(self, name, value):
        if isinstance(value, glm.mat4x4):
            value = value.to_list()
        else:
            value = value.m
        pos = glGetUniformLocation(self.program, name.encode('ascii'))
        glUniformMatrix4fv(pos, 1, GL_FALSE, (GLfloat * 16)(*sum(value, [])))

    def uniformi(self, name, value):
        pos = glGetUniformLocation(self.program, name.encode('ascii'))
        glUniform1i(pos, value)