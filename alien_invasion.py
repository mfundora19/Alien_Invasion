import sys
import pygame

from time import sleep
from random import randint
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from button import Button


class AlienInvasion:
    '''Overall class to manage game assets and behavior'''

    def __init__(self):
        '''Initialize the game, and create game resources'''
        
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption('Alien Invasion')

        # Start Alien Invasion in an active state
        self.game_active = False

        # Make the Play button
        self.play_button = Button(self, "Play")

        # Create the Objects
        self.clock = pygame.time.Clock()
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_fleet()
        self._create_stars()

    def run_game(self):
        '''Start the main loop for the game'''

        while True:
            # Watch for keyboard and mouse events.
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()


            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        '''Respond to keypresses and mouse events.'''

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
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
    def _check_play_button(self, mouse_pos):
        '''Start a new game when the player clicks play'''

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.stats.reset_stats()
            self.game_active = True

            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()

    def _fire_bullet(self):
        '''Create a new bullet and add it to the bullets group'''

        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        '''Create the fleet of aliens'''

        # Create an alien and keep adding aliens until there's no room left
        # Spacing b\w aliens is one alien width, one alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2*alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2*alien_width

            # Finished a row; reset x value, and increment y value
            current_x = alien_width
            current_y += 2*alien_height
    def _create_stars(self):
        '''Create a set of stars in the sky in a grid-aligned pattern with random offsets.'''
        
        # Define the spacing between stars
        grid_spacing_x = 150  # Adjust for horizontal spacing between stars
        grid_spacing_y = 150  # Adjust for vertical spacing between stars

        # Calculate number of rows and columns based on screen dimensions
        num_cols = self.settings.screen_width // grid_spacing_x
        num_rows = self.settings.screen_height // grid_spacing_y
        
        # Loop through each grid cell and create a star with a slight random offset
        for row in range(num_rows):
            for col in range(num_cols):
                # Randomly decide whether to create a star in this cell
                if randint(0, 1):  # Randomly decide if a star should be created in this cell
                    new_star = Star()
                    
                    # Calculate grid-aligned position with random offset
                    x_pos = col * grid_spacing_x + randint(-10, 10)  # Random offset within +/- 10 pixels
                    y_pos = row * grid_spacing_y + randint(-10, 10)
                    
                    new_star.rect.x = x_pos
                    new_star.rect.y = y_pos
                    self.stars.add(new_star)

    def _update_bullets(self):
        '''Update position of bullets and get rid of old bullets'''

        # Update bullet position
        self.bullets.update()

        # Get rid of bullets that have gone off the screen.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Repopulating the Fleet
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

        # Check for any bullets that have hit aliens. If so, get rid of the bullet and the alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

    # Aliens
    def _create_alien(self, x_position, y_position):
        '''Create an alien and place it in the row'''
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    def _update_aliens(self):
        '''Update the positions of all aliens in the fleet if alien hit an edge'''
        self._check_fleet_edges()
        self.aliens.update()

        # Check for alien-ship collisions 
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look fro aliens hitting the bottom of the screen
        self._check_alien_bottom()

    def _check_alien_bottom(self):
        '''Check if any aliens have reached the bottom of the screen'''

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat the same as ship got hit
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        '''Respond appropriately if anu aliens have reached an edge'''

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        '''Drop the entire fleet and change fleet's direction'''

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed

        self.settings.alien_direction *= -1

    def _ship_hit(self):
        '''Respond to the ship being hit by an alien'''
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1

            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center  the ship
            self._create_fleet
            self.ship.center_ship()

            # Pause the game
            sleep(0.5)
        else:
            self.game_active = False

    def _update_screen(self):
        '''Update images on the screen, and flip the new screen.'''

        self.screen.fill(self.settings.bg_color)
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.stars.draw(self.screen)
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the Play button if game is inactive
        if not self.game_active:
            self.play_button.draw_button()
        

        # Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.

    ai = AlienInvasion()
    ai.run_game()