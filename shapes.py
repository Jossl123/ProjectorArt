import numpy as np
import pygame
class Shape:
    def __init__(self):
        self.position = np.array([0,0])
    def draw(self, screen):
        pass

class Rect(Shape, pygame.Rect):
    def __init__(self, x, y, w, h):
        Shape.__init__(self)
        pygame.Rect.__init__(self, x, y, w, h)
    def draw(self, screen):
        pass