import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    '''Overall class to manage game assets and behavior'''

    def __init__(self):
        '''Initialize the game, and create game resources'''
        
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption('Alien Invasion')

        # Create the Objects
        self.clock = pygame.time.Clock()
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        '''Start the main loop for the game'''

        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            self.ship.update()
            self.bullets.update()
            self._update_screen()

            # Get rud of bullets that have gone off the screen.
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            
            
            self.clock.tick(60)

    def _check_events(self):
        '''Respond to keypresses and mouse events.'''

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        '''Respond to keypresses'''

        # Move the ship to the right 
        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        # Move the ship to the left 
        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # Move the ship up
        elif event.key == pygame.K_w or event.key == pygame.K_UP:
            self.ship.moving_up = True
        # Move the ship down
        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        # Fire the bullets
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # Quit the game
        elif event.key == pygame.K_q:
            sys.exit()
    def _check_keyup_events(self, event):
        '''Respond to key releases'''

        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_w or event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        '''Create a new bullet and add it to the bullets group'''

        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        '''Create the fleet of aliens'''

        #Make alien
        alien = Alien(self)
        self.aliens.add(alien)

    def _update_screen(self):
        '''Update images on the screen, and flip the new screen.'''

        self.screen.fill(self.settings.bg_color)
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.

    ai = AlienInvasion()
    ai.run_game()