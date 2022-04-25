import pyglet
from pyglet.gl import *
import glm
from src.utility.raycast import *
import src.utility.debug as Debug
from src.utility.actions import *

import math


class Events:
    dt = 0
    curFrame = 0
    keys = {}
    pressed = {}
    hideMouse = False
    camera = None
    mouseX = 0
    mouseY = 0
    speed = 10
    sens = 0.1
    deltaX = 90
    deltaY = 0
    updateBlock = []
    closeWindow = False

    @classmethod
    def update(cls, dt):
        if cls.clicked(pyglet.window.key.A):
            if isinstance(cls.camera.pos, glm.vec3):
                cls.camera.pos -= glm.normalize(glm.cross(cls.camera.dir, cls.camera.up)) * dt * cls.speed
            else:
                cls.camera.pos -= (cls.camera.dir * cls.camera.up).normalize() * dt * cls.speed
        if cls.clicked(pyglet.window.key.D):
            if isinstance(cls.camera.pos, glm.vec3):
                cls.camera.pos += glm.normalize(glm.cross(cls.camera.dir, cls.camera.up)) * dt * cls.speed
            else:
                cls.camera.pos += (cls.camera.dir * cls.camera.up).normalize() * dt * cls.speed
        if cls.clicked(pyglet.window.key.W):
            cls.camera.pos += cls.camera.dir * dt * cls.speed
        if cls.clicked(pyglet.window.key.S):
            cls.camera.pos -= cls.camera.dir * dt * cls.speed
        if cls.clicked(pyglet.window.key.SPACE):
            cls.camera.pos += cls.camera.up * dt * cls.speed
        if cls.clicked(pyglet.window.key.LSHIFT):
            cls.camera.pos -= cls.camera.up * dt * cls.speed

        if cls.justClicked(pyglet.window.key.TAB):
            cls.firstMouse = True
            cls.hideMouse = not cls.hideMouse

        if cls.justClicked(pyglet.window.key.ESCAPE):
            cls.closeWindow = True

        cls.curFrame += 1

    @classmethod
    def clicked(cls, key):
        try:
            return cls.pressed[key]
        except:
            return 0

    @classmethod
    def justClicked(cls, key):
        try:
            return cls.pressed[key] and cls.keys[key] == cls.curFrame
        except:
            return 0

    @classmethod
    def on_resize(cls, width, height):
        glViewport(0, 0, width, height)

    @classmethod
    def on_key_press(cls, symbol):
        cls.pressed[symbol] = 1
        cls.keys[symbol] = cls.curFrame

    @classmethod
    def on_key_release(cls, symbol):
        cls.pressed[symbol] = 0

    @classmethod
    def on_mouse_scroll(cls, scroll_y):
        if cls.speed < 6:
            cls.speed += scroll_y * 0.5
        else:
            cls.speed += scroll_y * 2

    @classmethod
    def on_mouse_press(cls, button):
        normal = [0, 0, 0]
        coords = Raycast.hit_ray_new(cls.camera.pos, cls.camera.dir, 50, normal)

        if coords[0] == coords[1] == coords[2] == 1e9:
            return

        if button == 1:
            cls.updateBlock.append([coords[0], coords[1], coords[2], 1])
        else:
            cls.updateBlock.append([coords[0] + normal[0],
                                    coords[1] + normal[1],
                                    coords[2] + normal[2], 2])

    @classmethod
    def on_mouse_moved(cls, dx, dy):
        if not cls.hideMouse:
            return

        dx *= cls.sens
        dy *= cls.sens
        cls.deltaX += dx
        cls.deltaY += dy

        if cls.deltaY > 89:
            cls.deltaY = 89
        if cls.deltaY < -89:
            cls.deltaY = -89

        # direction = Vector(
        #     math.cos(glmath.radians(cls.deltaX)) * math.cos(glmath.radians(cls.deltaY)),
        #     math.sin(glmath.radians(cls.deltaY)),
        #     math.sin(glmath.radians(cls.deltaX)) * math.cos(glmath.radians(cls.deltaY))
        # )
        # cls.camera.dir = direction.normalize()
        direction = glm.vec3(
            math.cos(glm.radians(cls.deltaX)) * math.cos(glm.radians(cls.deltaY)),
            math.sin(glm.radians(cls.deltaY)),
            math.sin(glm.radians(cls.deltaX)) * math.cos(glm.radians(cls.deltaY))
        )
        cls.camera.dir = glm.normalize(direction)
