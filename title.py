from pygame import font

class Title:
    def __init__(self, game, msg, center, text_size = 200, text_color = (255, 255, 255)):
        # screen
        self.screen = game.screen

        # text
        self.text_color = text_color
        self.txt = msg
        font.init()
        self.font = font.SysFont(None, text_size)
        self._prep_msg(msg, center)

    def _prep_msg(self, msg, center):
        if msg == str(msg):
            self.msg_image = self.font.render(msg, True, self.text_color, None)
        else:
            self.msg_image = msg

        self.rect = self.msg_image.get_rect()
        self.rect.center = center

    def draw(self):
        self.screen.blit(self.msg_image, self.rect)