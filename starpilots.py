import sys
import pygame

# from pathlib import Path
# import json

from settings import Settings
from entity import Entity




class Game:
    def __init__(self):
        # basic
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Starpilots")

        # entities
        self.entities = pygame.sprite.Group()

        # asteroids
        self.entities.add(Entity(self, 'asteroid1', [700, 475], 0, 5, 0, 0))
        self.entities.add(Entity(self, 'asteroid2', [900, 475], 0, 0, 5, 5))
        self.entities.add(Entity(self, 'asteroid3', [500, 475], 0, 0, 0, 5))
        self.entities.add(Entity(self, 'asteroid4', [300, 475], 0, 45, 5, 0))


    def run(self):
        while True:
            self._update()
            self._check_events()
            self.clock.tick(60)


    """draw screen"""
    def _update(self):
        self.screen.fill((0, 0, 0))
        self._draw_entities()
        pygame.display.flip()

    def _draw_entities(self):
        for entity in self.entities:
            entity.update()
            entity.draw()

    
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