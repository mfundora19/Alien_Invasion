class Settings:
    '''A class to store all settings for Alien Invasion.'''

    def __init__(self):
        '''Initialize the game's settings'''

        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (3, 6, 55)

        # Ship Settings
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (200, 60, 60)
        self.bullet_allowed = 5

        # Aliens Settings
        self.alien_drop_speed = 10

        # How quickly the ame speeds up
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        '''Initialize settings that change throughout the game'''

        self.ship_speed = 3.5
        self.bullet_speed = 4
        self.alien_speed = 1.0
        self.alien_direction = 1 # (1 - Right) (2 - Left)
        self.alien_points = 10
    
    def increase_speed(self):
        '''Increase speed settings'''

        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
    
