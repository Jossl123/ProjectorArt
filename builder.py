import pygame
import numpy as np
import taichi as ti
from enum import Enum
from shapes import Rect, Circle
from audiovisual import Video
# settings;
res = width, height = 1920, 1080 # with modern video card with CUDA support - increase res '1600, 900' and set 'ti.init(arch=ti.cuda)'

class Action(Enum):
    NOTHING = 0
    CREATING_SHAPE = 1
    MOVING_SHAPE = 2
    CHOOSING_SHAPE = 3
    CHOOSING_FILE = 4

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

    # def control(self):
    #     pressed_key = pygame.key.get_pressed()
    #     dt = self.delta_time()
    #     # movement
    #     if pressed_key[pygame.K_a]:pass
    #     if pressed_key[pygame.K_d]:pass
    #     if pressed_key[pygame.K_w]:pass
    #     if pressed_key[pygame.K_s]:pass
    def right_click(self, mouse_pos):
        mouse_pos = np.array(mouse_pos)
        for index, shape in enumerate(self.shapes):
            if shape.point_inside(mouse_pos):
                #self.action = Action.CHOOSING_FILE
                #self.action_param = {"index":index}
                # file_selection = pygame.UIFileDialog(rect=Rect(0, 0, 300, 300), manager=manager, initial_file_path='C:\\')
                # if event.ui_element == file_selection.ok_button:
                #     file_path = file_selection.current_file_path
                if not shape.file:shape.file = Video("./videos/abstract_loop.mp4")
                else : shape.file = None
                continue
            
    def click(self, mouse_pos):
        mouse_pos = np.array(mouse_pos)
        match self.action:
            case Action.NOTHING:
                for index, shape in enumerate(self.shapes):
                    if shape.point_inside(mouse_pos):
                        self.action = Action.MOVING_SHAPE
                        self.action_param = {"index":index,"start_pos": mouse_pos}
                        continue
                if self.action == Action.NOTHING:
                    self.action = Action.CHOOSING_SHAPE
                    self.action_param = {"mouse_pos": mouse_pos}
            case Action.CREATING_SHAPE:
                self.shapes.append(self.action_param["shape"].modify(mouse_pos))
                self.action = Action.NOTHING
                self.action_param = None
            case Action.MOVING_SHAPE:
                self.action = Action.NOTHING
                self.action_param = None
            case Action.CHOOSING_SHAPE:
                dir = mouse_pos - self.action_param["mouse_pos"]
                mp = self.action_param["mouse_pos"]
                if np.linalg.norm(dir) <= 40:
                    shape = None
                    if dir[0]<0:shape=Rect(mp[0], mp[1], mp[0] + dir[0], mp[1] + dir[1])
                    else : shape = Circle(mp[0], mp[1], np.linalg.norm(dir))
                    self.action = Action.CREATING_SHAPE
                    self.action_param = {"mouse_pos": mp, "shape": shape}
                else:
                    self.action = Action.NOTHING
                    self.action_param = None

    def update(self):
        #self.render()
        #self.screen_array = self.screen_field.to_numpy()
        match self.action:
            case Action.MOVING_SHAPE:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos = np.array(mouse_pos)
                self.shapes[self.action_param["index"]].move(self.action_param["start_pos"]-mouse_pos)
                self.action_param["start_pos"] = mouse_pos

    def draw(self):
        #pygame.surfarray.blit_array(self.app.screen, self.screen_array)
        for shape in self.shapes:
            shape.draw(self.app.screen)
            #pygame.draw.rect(self.app.screen, (0,0,200), shape)
        match self.action:
            case Action.CREATING_SHAPE:
                r = self.action_param["shape"].modify(pygame.mouse.get_pos())
                r.draw(self.app.screen)
                #pygame.draw.rect(self.app.screen, (0,200,0), r)
                #pygame.draw.rect(self.app.screen, (0,100,0), pygame.Rect(r.left+2, r.top+2, r.width -4, r.height - 4))
            case Action.MOVING_SHAPE:
                self.shapes[self.action_param["index"]].draw(self.app.screen)
            case Action.CHOOSING_SHAPE:
                pygame.draw.circle(self.app.screen, (100,100,100), self.action_param["mouse_pos"], 40)
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
                    if i.button == 1:self.drawing.click(pygame.mouse.get_pos())
                    elif i.button == 3:self.drawing.right_click(pygame.mouse.get_pos())
            self.clock.tick(60)
            pygame.display.set_caption(f'FPS: {self.clock.get_fps() :.2f}')
        for i in range(len(self.drawing.shapes)):
            print(self.drawing.shapes[i])
            
if __name__ == '__main__':
    app = App()
    app.run()