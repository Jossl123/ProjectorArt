import pygame
import numpy as np
import cv2

class Image:
    def __init__(self, file):
        pass
    
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
