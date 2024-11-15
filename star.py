from random import randint
import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    '''A class that represent a single star in the sky (screen)'''

    def __init__(self):
        '''Initialize a star in a random position of the board '''

        super().__init__()
        
        self.image = pygame.image.load('images/sky_star.bmp')
        self.rect = self.image.get_rect()

