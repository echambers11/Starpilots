import pygame
from pygame.sprite import Sprite
from random import randint

class Star(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.screen_size = game.screen_size

        x = randint(0, self.screen_size[0])
        y = randint(0, self.screen_size[1])
        self.rect = pygame.rect.Rect(x, y, 2, 2)

    def draw_star(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)