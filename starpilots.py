import sys
import pygame

from pathlib import Path
import json

from settings import Settings




class Game:
    def __init__(self):
        # basic
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Starpilots")

    def run(self):
        while True:
            self._update()
            self._check_events()
            self.clock.tick(60)


    """draw screen"""
    def _update(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    
    """events"""
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._check_keydown(event)

    def _check_keydown(self, event):
        pass





if __name__ == '__main__':
    game = Game()
    game.run()