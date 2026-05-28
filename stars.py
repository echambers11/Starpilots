import pygame
from pygame.sprite import Sprite
from settings import Settings
from random import randint

class Star(Sprite):
    def __init__(self, game):
        super().__init__()
        self.settings = Settings()
        self.screen = game.screen

        x = randint(0, self.settings.screen_width)
        y = randint(0, self.settings.screen_height)
        self.rect = pygame.rect.Rect(x, y, 2, 2)

    def draw_star(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)