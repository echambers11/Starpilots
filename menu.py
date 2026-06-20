from title import Title

class Menu:
    '''initialization'''
    def __init__(self, game, title, button, info):
        self.screen = game.screen
        self.settings = game.settings
        self.title = Title(game, title, (self.settings.screen_width // 2, 130))
        self.button = button
        self.active = False
        self._init_info(info)

    def _init_info(self, info):
        self.info = []
        i = 0
        for x in info:
            self.info.append(Title(self, x, (self.settings.screen_width / 2, 260 + 45 * i), 45))
            i += 1

    '''draw the menu'''
    def draw(self):
        self.title.draw()
        for info in self.info:
            info.draw()

    