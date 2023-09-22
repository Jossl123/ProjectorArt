import pygame
import numpy as np
import taichi as ti
from enum import Enum
# settings
res = width, height = 800, 450 # with modern video card with CUDA support - increase res '1600, 900' and set 'ti.init(arch=ti.cuda)'

class Action(Enum):
    NOTHING = 0
    CREATING_SHAPE = 1
    MOVING_SHAPE = 2

@ti.data_oriented
class Drawing:
    def __init__(self, app):
        self.app = app
        self.screen_array = np.full((width, height, 3), [0, 0, 0], dtype=np.uint32)
        ti.init(arch=ti.cpu)
        self.screen_field = ti.Vector.field(3, ti.uint32, (width, height))
        self.app_speed = 1 / 4000
        self.prev_time = pygame.time.get_ticks()

        self.shapes = []
        self.action = Action.NOTHING
        self.action_param = None

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

    def click(self, mouse_pos):
        match self.action:
            case Action.NOTHING:
                for index, shape in enumerate(self.shapes):
                    if shape.collidepoint(mouse_pos):
                        self.action = Action.MOVING_SHAPE
                        self.action_param = {"index":index,"start_pos": mouse_pos}
                        continue
                if self.action == Action.NOTHING:
                    self.action = Action.CREATING_SHAPE
                    self.action_param = mouse_pos
            case Action.CREATING_SHAPE:
                self.shapes.append(mouse_poses_to_rect(self.action_param, mouse_pos))
                self.action = Action.NOTHING
                self.action_param = None
            case Action.MOVING_SHAPE:
                self.action = Action.NOTHING
                self.action_param = None

    def update(self):
        self.render()
        self.screen_array = self.screen_field.to_numpy()
        match self.action:
            case Action.MOVING_SHAPE:
                mouse_pos = pygame.mouse.get_pos()
                self.shapes[self.action_param["index"]].x -= self.action_param["start_pos"][0] - mouse_pos[0]
                self.shapes[self.action_param["index"]].y -= self.action_param["start_pos"][1] - mouse_pos[1]
                self.action_param["start_pos"] = mouse_pos

    def draw(self):
        pygame.surfarray.blit_array(self.app.screen, self.screen_array)
        for shape in self.shapes:
            pygame.draw.rect(self.app.screen, (0,0,200), shape)
        match self.action:
            case Action.CREATING_SHAPE:
                pygame.draw.rect(self.app.screen, (0,200,0), mouse_poses_to_rect(self.action_param, pygame.mouse.get_pos()))
            case Action.MOVING_SHAPE:
                pygame.draw.rect(self.app.screen, (0,200,0), self.shapes[self.action_param["index"]])
    def run(self):
        self.update()
        self.draw()

def mouse_poses_to_rect(mouse_pos1, mouse_pos2):
    x=mouse_pos1[0]
    y=mouse_pos1[1]
    w=mouse_pos2[0] - x 
    h=mouse_pos2[1] - y
    if w < 0:
        w *= -1
        x -= w
    if h < 0:
        h *= -1
        y -= h
    return pygame.Rect(x, y, w, h)

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode(res, pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.drawing = Drawing(self)
        self.running = True

    def run(self):
        while self.running:
            self.screen.fill('black')
            self.drawing.run()
            pygame.display.flip()
            
            for i in pygame.event.get():
                if i.type == pygame.QUIT:self.running = False
                elif i.type == pygame.MOUSEBUTTONUP:
                    self.drawing.click(pygame.mouse.get_pos())
            self.clock.tick()
            pygame.display.set_caption(f'FPS: {self.clock.get_fps() :.2f}')
        print(self.drawing.shapes)
if __name__ == '__main__':
    app = App()
    app.run()