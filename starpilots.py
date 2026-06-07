import sys
import pygame

# from pathlib import Path
# import json

from settings import Settings
from starship import Starship
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
        
        # starships
        self.p1_turn = 0
        self.p1_accel = 0
        self.p1 = Starship(self, 1, [900, 300], 90, 0, 0, 0, 1000)
        self.entities.add(self.p1)

        # bullets
        self.bullets = pygame.sprite.Group()

    def run(self):
        while True:
            self._update()
            self._check_events()
            self._accl_entities()
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
        for bullet in self.bullets:
            bullet.update(self.entities)
            bullet.draw_bullet()

    
    """events"""
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(self.entities)
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._check_keydown(event)
            if event.type == pygame.KEYUP:
                self._check_keyup(event)

    def _check_keydown(self, event):
        if event.key == pygame.K_LEFT:
            self.p1_turn = self.settings.ship_turn
        elif event.key == pygame.K_RIGHT:
            self.p1_turn = -self.settings.ship_turn
        elif event.key == pygame.K_UP:
            self.p1.accl = True
            self.p1_accel = self.settings.ship_accel
        elif event.key == pygame.K_DOWN:
            self.bullets.add(self.p1.shoot())
    
    def _check_keyup(self, event):
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            self.p1_turn = 0
        elif event.key == pygame.K_UP:
            self.p1.accl = False
            self.p1_accel = 0

    def _accl_entities(self):
        self.p1.turn(self.p1_turn)
        self.p1.acclerate(self.p1_accel)





if __name__ == '__main__':
    game = Game()
    game.run()