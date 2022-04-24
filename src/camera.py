from glmath import *
import glm


class Camera:
    def __init__(self, **kwargs):
        self.proj = Matrix.projection(**kwargs)
        # self.pos = Vector(0, 7, 0)
        # self.dir = Vector(0, 0, -1)
        # self.up = Vector(0, 1, 0)
        # self.lookAt = Matrix.lookat(self.pos, self.dir + self.pos, self.up)

        self.pos = glm.vec3(0, 0, 0)
        self.dir = glm.vec3(0, 0, 1)
        self.up = glm.vec3(0, 1, 0)
        self.lookAt = glm.lookAt(self.pos, self.dir + self.pos, self.up)

    def update_matrix(self):
        #self.lookAt = Matrix.lookat(self.pos, self.dir + self.pos, self.up)
        self.lookAt = glm.lookAt(self.pos, self.dir + self.pos, self.up)
