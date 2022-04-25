import time


from src.events import *
from src.glmath import *
from src.graphics.shader import *
from src.graphics.texture import *
from src.camera import *
from src.utility.raycast import *
import src.utility.debug as Debug
from src.world.chunk import *
import src.utility.variables as util
from src.world.chunkManager import *
from src.utility.actions import *


class Window(pyglet.window.Window):
    def __init__(self, shader, camera, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camera = camera
        self.shader = shader
        self.world = ChunkManager(2, 2)
        self.worldRenderer = Renderer(util.global_buffer, [], [3])
        util.global_buffer.clear()
        Raycast.install(self.world)
        Events.camera = self.camera
        Events.mouseX = self.width / 2
        Events.mouseY = self.height / 2
        glEnable(GL_DEPTH_TEST)
        pyglet.clock.schedule_interval(self.update, 1.0 / 1000)

        self.crossRenderer = LineRenderer(geom.cross, [3])
        self.crosshader = Shader("../res/shaders/cross.vert", "../res/shaders/cross.frag")

        Debug.memory_usage(self.world)

    def on_draw(self):
        glClearColor(*util.get_color(146, 188, 222), 1)
        self.clear()
        self.shader.use()
        Texture.use()
        self.shader.uniformi("texture_array", 0)
        self.shader.uniformm("proj", self.camera.proj)
        self.shader.uniformm("view", self.camera.lookAt)
        #Debug.log(self.camera.pos)
        self.worldRenderer.draw()
        self.crosshader.use()
        self.crossRenderer.draw()

    def update(self, delta_time):
        if Events.closeWindow:
            self.close()
            return
        self.set_exclusive_mouse(Events.hideMouse)
        Events.update(delta_time)
        self.camera.update_matrix()
        if len(Events.updateBlock) > 0:
            for op in Events.updateBlock:
                chunk = self.world.get_chunk(op[0], op[1], op[2])
                if chunk is None:
                    continue
                vx = op[0] - chunk.posX * W
                vz = op[2] - chunk.posZ * D
                y = op[1]
                if op[3] == 1:
                    chunk.voxels[vz + D * (vx + W * y)] = 0
                    chunk.mesh.remove_block(vx, y, vz)
                else:
                    chunk.voxels[vz + D * (vx + W * y)] = 2
                    chunk.mesh.place_block(vx, y, vz)
            self.worldRenderer.update(updated_buffer, to_update)
            Events.updateBlock.clear()
            to_update.clear()
            clear_updated_buffer()

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

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        Events.on_mouse_scroll(scroll_y)


class Game:
    def __init__(self, *args, **kwargs):
        self.camera = Camera(fov=70, width=kwargs.get("width"), height=kwargs.get("height"), near=0.1, far=1000)
        self.shader = Shader("../res/shaders/main.vert", "../res/shaders/main.frag")
        self.window = Window(self.shader, self.camera, *args, **kwargs)
        self.window.set_location(200, 50)
        Texture.create(32, 32, 3, "D:/programming/Python/newmine/res/textures")
        Texture.add_texture("void.png")
        Texture.add_texture("green.png")
        Texture.add_texture("orange.png")
        Texture.generate_mipmaps()

    def run(self):
        pyglet.app.run()


if __name__ == "__main__":
    game = Game(width=1000, height=800, caption="Minecraft", resizable=True, vsync=False)
    game.run()
