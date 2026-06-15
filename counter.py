from pygame import font
from title import Title

class Counter(Title):
    def __init__(self, game, name, center, stat, text_color = (255, 255, 255)):
        super().__init__(game, f"{name}: {stat}", center, 30, text_color)
        self.stat = stat
        self.name = name

    def change_stat(self, stat):
        self.stat = stat
        self._prep_msg(f"{self.name}: {self.stat}", self.rect.center)