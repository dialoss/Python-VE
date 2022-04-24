import ctypes

from pyglet import *
from pyglet.gl import *


def create_texture(target, path):
    img = pyglet.image.load(path).get_image_data()

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img.get_data("RGBA"))
    glGenerateMipmap(GL_TEXTURE_2D)


class Texture:
    textures = []
    texture_array = None
    width = 0
    height = 0
    count = 0
    path = ""

    @classmethod
    def create(cls, width, height, count, path):
        cls.width = width
        cls.height = height
        cls.count = count
        cls.path = path
        cls.texture_array = GLuint(0)
        glGenTextures(1, ctypes.byref(cls.texture_array))
        glBindTexture(GL_TEXTURE_2D_ARRAY, cls.texture_array)

        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glTexImage3D(
            GL_TEXTURE_2D_ARRAY, 0, GL_RGBA,
            cls.width, cls.height, cls.count,
            0, GL_RGBA, GL_UNSIGNED_BYTE, None
        )

    @classmethod
    def use(cls):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D_ARRAY, cls.texture_array)

    @classmethod
    def add_texture(cls, name):
        if not name in cls.textures:
            cls.textures.append(name)
            texture_img = pyglet.image.load(f"{cls.path}/{name}").get_image_data()
            glBindTexture(GL_TEXTURE_2D_ARRAY, cls.texture_array)

            glTexSubImage3D(
                GL_TEXTURE_2D_ARRAY, 0,
                0, 0, cls.textures.index(name),
                cls.width, cls.height, 1,
                GL_RGBA, GL_UNSIGNED_BYTE,
                texture_img.get_data("RGBA")
            )

    @classmethod
    def generate_mipmaps(cls):
        glGenerateMipmap(GL_TEXTURE_2D_ARRAY)