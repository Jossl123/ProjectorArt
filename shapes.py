import numpy as np
import pygame
from audiovisual import Video

class Shape:
    def __init__(self):
        self.file = None
        self.active_file = True
    def draw(self, screen):pass
    def modify(self, mouse_pos):pass
    def point_inside(self, p):pass
    def move(self, p):pass
    def __str__(self):
        return "<shape()>"
    def __hash__(self) -> int:
        return 0
    
class Rect(Shape, pygame.Rect):
    def __init__(self, x, y, w, h):
        Shape.__init__(self)
        self.file = Video("./videos/abstract_loop.mp4")
        self.start_pos=np.array([x, y])
        pygame.Rect.__init__(self, x, y, w, h)
        self.color = np.array([0,200,0])
    def draw(self, screen, pixel_array):
        if not self.file or not self.active_file :
            self.pixel_array = pixel_array
            self.abstract_art(screen)
            return
        img = self.file.get_image()
        img = pygame.transform.scale(img, self.size)
        screen.blit(img, self.topleft, pygame.Rect(0,0,self.width,self.height))
        #screen.blit(self.file.get_image(), self.topleft)
    
    def abstract_art(self, screen):
        pygame.draw.rect(screen, self.color, self,2)
        s = pygame.Surface(self.size)
        s.set_alpha(128)
        s.fill( np.divide(self.color, 2))
        screen.blit(s, self.topleft)
        self.color = np.array([0,200,0])
        
    def modify(self, mouse_pos):
        x=self.start_pos[0]
        y=self.start_pos[1]
        w=mouse_pos[0] - x 
        h=mouse_pos[1] - y
        if w < 0:
            w *= -1
            x -= w
        if h < 0:
            h *= -1
            y -= h
        self.left = x
        self.top = y
        self.width = w
        self.height = h
        self.color = (0,100,0)
        return self
    def point_inside(self, p):
        return self.collidepoint(p)
    def move(self, p):
        self.x -= p[0]
        self.y -= p[1]
    def __str__(self):
        return "<rect("+str(self.x)+","+str(self.y)+","+str(self.width)+","+str(self.height)+")>"
    def __hash__(self) -> int:
        return self.x **8 + self.y ** 4 + self.width ** 2 + self.height

class Circle(Shape):
    def __init__(self, x, y, r=0):
        Shape.__init__(self)
        self.center = np.array((x, y))
        self.file = Video("./videos/abstract_loop.mp4")
        self.radius = r
        self.color = np.array((200,0,0))
    def draw(self, screen, pixel_array):
        pygame.draw.circle(screen, self.color, self.center, self.radius)
        t = 1
        pygame.draw.circle(screen, np.divide(self.color, 2), self.center, self.radius-t)
        self.color = np.array((200,0,0))
        if not self.file or not self.active_file:
            return
        image = self.file.get_image()
        image = pygame.transform.scale(image, (self.radius, self.radius))
        screen.blit(image, self.center, pygame.Rect(0,0,self.radius,self.radius))

    def modify(self, mouse_pos):
        self.color = np.array((100,0,0))
        self.radius = np.linalg.norm(self.center - mouse_pos)
        return self
    def point_inside(self, p):
        return np.linalg.norm(p - self.center) <= self.radius
    def move(self, p):
        self.center = self.center - p
    def __str__(self):
        return "<circle("+str(self.center[0])+","+str(self.center[1])+","+str(self.radius)+")>"