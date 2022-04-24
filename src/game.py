import time

from events import *
from glmath import *
from src.graphics.shader import *
from src.graphics.texture import *
from camera import *
from src.utility.raycast import *
from utility.debug import *
from src.world.chunk import *
import src.utility.variables as util
from world.chunkManager import *
from src.utility.actions import *


class Window(pyglet.window.Window):
    def __init__(self, shader, camera, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camera = camera
        self.shader = shader
        self.world = ChunkManager(2, 2)
        Raycast.install(self.world)
        Events.camera = self.camera
        Events.mouseX = self.width / 2
        Events.mouseY = self.height / 2
        glEnable(GL_DEPTH_TEST)
        pyglet.clock.schedule_interval(self.update, 1.0 / 1000)

        self.crossRenderer = Renderer(geom.cross, [], [3])
        self.crosshader = Shader("../res/shaders/cross.vert", "../res/shaders/cross.frag")

    def on_draw(self):
        glClearColor(*util.get_color(146, 188, 222), 1)
        self.clear()
        self.shader.use()
        Texture.use()
        self.shader.uniformi("texture_array", 0)
        self.shader.uniformm("proj", self.camera.proj)
        self.shader.uniformm("view", self.camera.lookAt)
        #Debug.log(self.camera.pos)
        for coord, chunk in ChunkManager.chunks.items():
            x = coord // 100
            z = coord % 100
            model = Matrix.translate(Vector(x * W, 0, z * D))
            self.shader.uniformm("model", model)
            chunk.renderer.draw()

        self.crosshader.use()
        self.crossRenderer.draw()

    def update(self, delta_time):
        self.set_exclusive_mouse(Events.hideMouse)
        Events.update(delta_time)
        self.camera.update_matrix()
        update_chunk = []
        if len(Events.updateBlock) > 0:
            for op in Events.updateBlock:
                chunk = self.world.get_chunk(op[0], op[1], op[2])
                vx = op[0] - chunk.posX * W
                vz = op[2] - chunk.posZ * D
                y = op[1]
                if op[3] == 1:
                    chunk.voxels[vz + D * (vx + W * y)] = 0
                    chunk.mesh.remove_block(vx, y, vz)
                else:
                    chunk.voxels[vz + D * (vx + W * y)] = 2
                    chunk.mesh.place_block(vx, y, vz, 2)
                if not chunk in update_chunk:
                    update_chunk.append(chunk)
        Events.updateBlock.clear()
        for chunk in update_chunk:
            chunk.renderer.update(chunk.mesh.vBuffer, chunk.mesh.iBuffer)

    def on_resize(self, width, height):
        Events.on_resize(width, height)

    def on_key_press(self, symbol, modifiers):
        Events.on_key_press(symbol)

    def on_key_release(self, symbol, modifiers):
        Events.on_key_release(symbol)

    def on_mouse_press(self, x, y, button, modifiers):
        Events.on_mouse_press(button)

    def on_mouse_motion(self, x, y, dx, dy):
        Events.on_mouse_moved(dx, dy)


class Game:
    def __init__(self, *args, **kwargs):
        self.camera = Camera(fov=70, width=kwargs.get("width"), height=kwargs.get("height"), near=0.1, far=1000)
        self.shader = Shader("../res/shaders/main.vert", "../res/shaders/main.frag")
        self.window = Window(self.shader, self.camera, *args, **kwargs)
        self.window.set_location(0, 30)
        Texture.create(32, 32, 3, "D:/Programming/newmine/res/textures")
        Texture.add_texture("void.png")
        Texture.add_texture("green.png")
        Texture.add_texture("orange.png")
        Texture.generate_mipmaps()

    def run(self):
        pyglet.app.run()


if __name__ == "__main__":
    game = Game(width=800, height=600, caption="Minecraft", resizable=True, vsync=False)
    game.run()
