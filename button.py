from pygame import Rect, font


class Button:

    def __init__(self, game, msg, center, wid, hgt, button_color = (50, 50, 255), text_color = (255, 255, 255)):
        # screen
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # size and color
        self.width, self.height = wid, hgt
        self.button_color = button_color
        self.text_color = text_color
        self.rect = Rect(0, 0, self.width, self.height)
        self.rect.center = center

        # text
        self.txt = msg
        font.init()
        self.font = font.SysFont(None, 48)
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        if msg == str(msg):
            self.msg_image = self.font.render(msg, True, self.text_color, None)
        else:
            self.msg_image = msg
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def is_pressed(self, pos):
        return self.rect.collidepoint(pos)