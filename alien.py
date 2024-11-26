import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''A class that represents a single alien in the fleet'''

    def __init__(self, ai_game):
        '''Initialize an alien and set its initial position'''

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image an get set the rect attributes
        self.image = pygame.image.load('images/alien_ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position 
        self.x = float(self.rect.x)
    
    def update(self):
        '''Move the alien to the right'''
        self.x += self.settings.alien_speed
        self.rect.x = self.x