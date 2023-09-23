import numpy as np
import pygame
class Shape:
    def __init__(self):pass
    def draw(self, screen):pass
    def modify(self, mouse_pos):pass
    def point_inside(self, p):pass

class Rect(Shape, pygame.Rect):
    def __init__(self, x, y, w, h):
        Shape.__init__(self)
        self.start_pos=np.array([x, y])
        pygame.Rect.__init__(self, x, y, w, h)
    def draw(self, screen):
        pygame.draw.rect(screen, (0,200,0), self)
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
        return self
    def point_inside(self, p):
        return self.collidepoint(p)
    def move(self, p):
        self.x -= p[0]
        self.y -= p[1]

class Circle(Shape):
    def __init__(self, x, y, r=0):
        Shape.__init__(self)
        self.center = np.array((x, y))
        self.radius = r
    def draw(self, screen):
        pygame.draw.circle(screen, (100,0,0), self.center, self.radius)
    def modify(self, mouse_pos):
        self.radius = np.linalg.norm(self.center - mouse_pos)
        return self
    def point_inside(self, p):
        return np.linalg.norm(p - self.center) <= self.radius
    def move(self, p):
        self.center = self.center - p