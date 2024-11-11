class Settings:
    '''A class to store all settings for Alien Invasion.'''

    def __init__(self):
        '''Initialize the game's settings'''

        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (3, 6, 55)

        # Ship Settings
        self.ship_speed = 2.5