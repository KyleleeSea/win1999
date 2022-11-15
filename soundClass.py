
from cmu_112_graphics import *
import pygame

class Sound(object):
    def __init__(self, path):
        self.path = path
        self.sound = pygame.mixer.Sound(path)

    def start(self, loops=1):
        self.loops = loops
        self.sound.play(loops=loops)

    # Stops the current sound from playing
    def stop(self):
        self.sound.stop()

    def changeVolume(self, volume):
        self.sound.set_volume(volume)