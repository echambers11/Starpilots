import pygame
from pygame.sprite import Sprite
from math import sin, cos, radians


class Entity(Sprite):
    '''basic functions'''
    def __init__(self, game, type, pos, angle, dir, velo, spin):
        super().__init__()
        # basic
        self.screen = game.screen
        self.settings = game.settings

        # pos + velo
        self.pos = pos
        self.angle = angle
        self.dir = dir
        self.velo = velo
        self.spin = spin

        # image
        self.type = type
        self.original_image = pygame.image.load(f'images/{type}.png')
        self.image = self.original_image
        self.rect = self.image.get_rect()

    def draw(self):
        self.rect.center = self.pos
        self.screen.blit(self.image, self.rect)


    '''motion'''
    def update(self):
        # spin
        if self.spin != 0:
            self.angle = (self.angle + self.spin) % 360
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect()
            # self.angle += self.spin
            # pygame.transform.rotate(self.image, self.spin)
            # self.rect = self.image.get_rect()
            # if self.angle > 360 or self.angle < -360:
            #     self.angle = self.angle % 360
        
        # move
        x_change = -sin(radians(self.dir)) * self.velo
        y_change = -cos(radians(self.dir)) * self.velo
        self.pos[0] += x_change
        self.pos[1] += y_change


    '''str'''
    def __str__(self):
        return f'<Entity {self.type} at {self.pos}>'