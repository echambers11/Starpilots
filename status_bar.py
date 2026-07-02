from pygame import Rect, font, draw

class StatusBar:
    def __init__(self, game, name, center, wid, hgt, max, stat, bar_color = (0, 255, 0), text_color = (255, 255, 255)):
        # screen
        self.screen = game.screen

        # stat info
        self.stat = stat
        self.max_stat = max

        # size and color
        self.width, self.height = wid, hgt
        self.color = bar_color
        self.text_color = text_color

        # rects
        self.outline_rect = Rect(0, 0, self.width, self.height)
        self.outline_rect.center = center
        self.bar_rect = Rect(0, 0, ((self.width - 8) * self.stat / self.max_stat), self.height - 8)
        self.bar_rect.center = self.outline_rect.center       
        self.bar_rect.left = self.outline_rect.left + 4

        # text
        self._prep_name(name)

    def _prep_name(self, name):
        # font
        self.txt = name
        font.init()
        self.font = font.SysFont(None, 30)

        # image
        self.msg_image = self.font.render(f"{name}: ", True, self.text_color, None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.outline_rect.center
        self.msg_image_rect.right = self.outline_rect.left - 5

    def change_stat(self, stat):
        self.stat = stat
        self.bar_rect.width = (self.width - 8) * self.stat / self.max_stat

    def draw(self):
        draw.rect(self.screen, (100, 100, 100), self.outline_rect, 4)
        draw.rect(self.screen, self.color, self.bar_rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)