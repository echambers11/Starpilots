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

        # menus
        self.controls_info = ['Move Forward: ^',
                              'Spin Left: <',
                              'Spin Right: >',
                              'Shoot: Space',
                              "The arrow keys do not",
                              "change your ship's velocity."]
        
        self.tips_info = ['You are the maroon, V-shaped ship.',
                          'Your goal is to destroy the enemies.',
                          'The enemies are all the other ships on the screen.',
                          'Avoid asteroids and lasers to stay alive.',
                          'You can shoot lasers to destroy enemies and asteroids.',
                          'The faster you go, the harder it is to control your ship.']