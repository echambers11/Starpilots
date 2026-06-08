class Settings():
    def __init__(self):
        # screen settings
        self.screen_width = 1400
        self.screen_height = 950
        self.star_count = 100

        # ship settings
        self.ship_accel = 0.1
        self.ship_turn = 0.1

        # laser settings
        self.bullet_color = (255, 0, 0)
        self.bullet_width = 2
        self.bullet_height = 15
        self.bullet_speed = 5

        # enemy settings
        self.enemy_max_speed = 3