import pygame
import numpy as np
import taichi as ti
import cv2

# settings
res = width, height = 1920, 1080 # with modern video card with CUDA support - increase res '1600, 900' and set 'ti.init(arch=ti.cuda)'

class Video:
    def __init__(self, file):
        self.video = cv2.VideoCapture(file)
        self.restart = True
        self.file = file
        self.position = np.array([0,0])
        self.success = False
        self.video_image = None
    
    def get_image(self):
        self.position[0]+=1
        self.success, self.video_image = self.video.read()
        if self.success:
            return pygame.image.frombuffer(
                self.video_image.tobytes(), self.video_image.shape[1::-1], "BGR")
        else:
            self.restart_video()
            return pygame.image.frombuffer(
                self.video_image.tobytes(), self.video_image.shape[1::-1], "BGR")

    def restart_video(self):
        self.video = cv2.VideoCapture(self.file)
        self.success, self.video_image = self.video.read()

    def get_fps(self):
        return self.video.get(cv2.CAP_PROP_FPS)

@ti.data_oriented
class Drawing:
    def __init__(self, app):
        self.app = app
        self.screen_array = np.full((width, height, 3), [0, 0, 0], dtype=np.uint32)
        # taichi architecture : ti.cpu, ti.cuda, ti.opengl, ti.vulkan, ti.metal
        ti.init(arch=ti.cpu)
        self.screen_field = ti.Vector.field(3, ti.uint32, (width, height))
        self.video = Video("./videos/the_rock_meme.mp4")
        self.app_speed = 1 / 4000
        self.prev_time = pygame.time.get_ticks()

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
        #self.render()
        #self.screen_array = self.screen_field.to_numpy()
        pass

    def draw(self):
        #pygame.surfarray.blit_array(self.app.screen, self.screen_array)
        self.app.screen.blit(self.video.get_image(), self.video.position)

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
            #clock.tick(video.get(cv2.CAP_PROP_FPS))
            self.screen.fill('black')
            self.drawing.run()
            pygame.display.flip()

            [exit() for i in pygame.event.get() if i.type == pygame.QUIT]
            self.clock.tick(self.drawing.video.get_fps())
            pygame.display.set_caption(f'FPS: {self.clock.get_fps() :.2f}')

if __name__ == '__main__':
    app = App()
    app.run()