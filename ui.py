import pygame
import numpy as np
from shapes import Rect, Circle
SHAPE_TOOl_SIZE = 40
def draw_shape_tool(screen, pos):
    pygame.draw.circle(screen, (100,100,100), pos, SHAPE_TOOl_SIZE)
    pygame.draw.circle(screen, (80,80,80), pos + np.array([SHAPE_TOOl_SIZE/2,0]), SHAPE_TOOl_SIZE/4)
    pygame.draw.rect(screen, (80,80,80), pygame.Rect(pos[0]-(SHAPE_TOOl_SIZE-SHAPE_TOOl_SIZE/4), pos[1]-SHAPE_TOOl_SIZE/4, SHAPE_TOOl_SIZE/2,SHAPE_TOOl_SIZE/2))
    pygame.draw.rect(screen, (80,80,80), pygame.Rect(pos[0]-1, pos[1]-SHAPE_TOOl_SIZE, 2,SHAPE_TOOl_SIZE*2))

def select_shape(mp, dir):
    if np.linalg.norm(dir) <= SHAPE_TOOl_SIZE:
        shape = None
        if dir[0]<0:shape=Rect(mp[0], mp[1], mp[0] + dir[0], mp[1] + dir[1])
        else : shape = Circle(mp[0], mp[1], np.linalg.norm(dir))
        return shape
    return None