import sys
import pygame

# from pathlib import Path
# import json

from settings import Settings
from asteroid import Asteroid
from stars import Star




class Game:
    def __init__(self):
        # basic
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Starpilots")

        # entities
        self._create_stars()
        self.entities = pygame.sprite.Group()

        # asteroids
        for i in range(0, 9):
            self.entities.add(Asteroid(self, 1, [i * 100, i * 100], 0, i*160, 1, 5, 5))


    def run(self):
        while True:
            self._update()
            self._check_events()
            self.clock.tick(60)

    
    '''create entities'''
    def _create_stars(self):
        self.stars = pygame.sprite.Group()
        for x in range(0, self.settings.star_count):
            self.stars.add(Star(self))


    """draw screen"""
    def _update(self):
        self.screen.fill((0, 0, 0))
        for star in self.stars.sprites():
            star.draw_star()
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
                print(self.entities)
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._check_keydown(event)

    def _check_keydown(self, event):
        pass





if __name__ == '__main__':
    game = Game()
    game.run()