import pygame as pg
import numpy as np
import taichi as ti

# settings
res = width, height = 800, 450 # with modern video card with CUDA support - increase res '1600, 900' and set 'ti.init(arch=ti.cuda)'

@ti.data_oriented
class Drawing:
    def __init__(self, app):
        self.app = app
        self.screen_array = np.full((width, height, 3), [0, 0, 0], dtype=np.uint32)
        # taichi architecture, you can use ti.cpu, ti.cuda, ti.opengl, ti.vulkan, ti.metal
        ti.init(arch=ti.cpu)
        # taichi fields
        self.screen_field = ti.Vector.field(3, ti.uint32, (width, height))
        # control settings
        


        # delta_time
        self.app_speed = 1 / 4000
        self.prev_time = pg.time.get_ticks()

    def delta_time(self):
        time_now = pg.time.get_ticks() - self.prev_time
        self.prev_time = time_now
        return time_now * self.app_speed

    @ti.kernel
    def render(self):
        for x, y in self.screen_field: # parallelization loop
            col = (x+y)%255
            self.screen_field[x, y] = [col, col, col]

    def control(self):
        pressed_key = pg.key.get_pressed()
        dt = self.delta_time()
        # movement
        if pressed_key[pg.K_a]:pass
        if pressed_key[pg.K_d]:pass
        if pressed_key[pg.K_w]:pass
        if pressed_key[pg.K_s]:pass

    def update(self):
        self.render()
        self.screen_array = self.screen_field.to_numpy()

    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)

    def run(self):
        self.update()
        self.draw()


class App:
    def __init__(self):
        self.screen = pg.display.set_mode(res, pg.SCALED)
        self.clock = pg.time.Clock()
        self.drawing = Drawing(self)

    def run(self):
        while True:
            self.screen.fill('black')
            self.drawing.run()
            pg.display.flip()

            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.clock.tick()
            pg.display.set_caption(f'FPS: {self.clock.get_fps() :.2f}')


if __name__ == '__main__':
    app = App()
    app.run()