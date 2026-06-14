from pygame import font

class Counter:
    def __init__(self, game, name, center, stat, text_color = (255, 255, 255)):
        # screen
        self.screen = game.screen

        # stat info
        self.stat = stat
        
        # text
        self.text_color = text_color
        self._prep_name(name, center)

    def _prep_name(self, name, center):
        # font
        self.txt = name
        font.init()
        self.font = font.SysFont(None, 30)

        # image
        self.msg_image = self.font.render(f"{name}: {self.stat}", True, self.text_color, None)
        self.rect = self.msg_image.get_rect()
        self.rect.center = center

    def change_stat(self, stat):
        self.stat = stat
        self._prep_name(self.txt, self.rect.center)

    def draw(self):
        self.screen.blit(self.msg_image, self.rect)