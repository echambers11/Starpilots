from pygame import font

class Title:
    def __init__(self, game, msg, center, text_color = (255, 255, 255)):
        # screen
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # text
        self.text_color = text_color
        self.txt = msg
        font.init()
        self.font = font.SysFont(None, 200)
        self._prep_msg(msg)

        # rect
        self.rect = self.msg_image.get_rect()
        self.rect.center = center

    def _prep_msg(self, msg):
        if msg == str(msg):
            self.msg_image = self.font.render(msg, True, self.text_color, None)
        else:
            self.msg_image = msg

    def draw(self):
        self.screen.blit(self.msg_image, self.rect)