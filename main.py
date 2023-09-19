import pygame
import numpy as np
import taichi as ti
import cv2

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
        
        self.restart_video()

        # delta_time
        self.app_speed = 1 / 4000
        self.prev_time = pygame.time.get_ticks()

    def restart_video(self):
        self.video = cv2.VideoCapture("the_rock_meme.mp4")
        self.success, self.video_image = self.video.read()


    def delta_time(self):
        time_now = pygame.time.get_ticks() - self.prev_time
        self.prev_time = time_now
        return time_now * self.app_speed

    @ti.kernel
    def render(self):
        for x, y in self.screen_field: # parallelization loop
            col = (x+y)%255
            self.screen_field[x, y] = [col, col, col]

    def control(self):
        pressed_key = pygame.key.get_pressed()
        dt = self.delta_time()
        # movement
        if pressed_key[pygame.K_a]:pass
        if pressed_key[pygame.K_d]:pass
        if pressed_key[pygame.K_w]:pass
        if pressed_key[pygame.K_s]:pass

    def update(self):
        # clock = pygame.time.Clock()
        # movie = pygame.movie.Movie('MELT.Mpg')
        # screen = pygame.display.set_mode(movie.get_size())
        # movie_screen = pygame.Surface(movie.get_size()).convert()

        # movie.set_display(movie_screen)
        # movie.play()

        self.render()
        self.screen_array = self.screen_field.to_numpy()

    def draw(self):
        pygame.surfarray.blit_array(self.app.screen, self.screen_array)
        self.success, self.video_image = self.video.read()
        if self.success:
            video_surf = pygame.image.frombuffer(
                self.video_image.tobytes(), self.video_image.shape[1::-1], "BGR")
            self.app.screen.blit(video_surf, (0, 0))
        else:
            self.restart_video()

    def run(self):
        self.update()
        self.draw()


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode(res, pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.drawing = Drawing(self)

    def run(self):
        while True:
            self.screen.fill('black')
            self.drawing.run()
            pygame.display.flip()

            [exit() for i in pygame.event.get() if i.type == pygame.QUIT]
            self.clock.tick()
            pygame.display.set_caption(f'FPS: {self.clock.get_fps() :.2f}')


if __name__ == '__main__':
    app = App()
    app.run()