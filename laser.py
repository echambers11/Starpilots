import pygame
from pygame.sprite import Sprite
from math import cos, sin, radians

class Polygon():
    def __init__(self, color, points):
        self.color = color
        self.points = points

    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.points)

    def move_points(self, x, y):
        positioned_points = []
        for point in self.points:
            positioned_point = ((point[0] + x),
                                (point[1] + y))
            positioned_points.append(positioned_point)
        self.points = positioned_points

        return self

class Laser(Sprite):
    def __init__(self, screen, settings, ship):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.color = self.settings.bullet_color
        self.speed = (self.settings.bullet_speed + ship.velo)

        # create points for slanted rectangle
        self.dir = ship.angle
        self.center = ship.pos

        width2 = self.settings.bullet_height*cos(radians(90-self.dir))
        width1 = self.settings.bullet_width*cos(radians(self.dir))
        width = width1 + width2

        height2 = self.settings.bullet_height*sin(radians(90-self.dir))
        height1 = self.settings.bullet_width*sin(radians(self.dir))
        height = height1 + height2

        points = [(self.center[0] - width/2, self.center[1] - height/2 + height1),
                  (self.center[0] - width/2 + width1, self.center[1] - height/2),
                  (self.center[0] + width/2, self.center[1] + height/2 - height1),
                  (self.center[0] + width/2 - width1, self.center[1] + height/2)]
        self.polygon = Polygon(self.color, points)

        # move out of way
        while self.check_collision(ship):
            self._move()

    def update(self, entities):
        self._move()

        # check collisions with entities
        for entity in entities:
            if self.check_collision(entity):
                entity.take_damage(5)
                self.kill()
                break

        # check if off screen
        if self.center[0] < 0 or self.center[0] > self.settings.screen_width:
            if self.center[1] < 0 or self.center[1] > self.settings.screen_height:
                self.kill()

    def _move(self):
        x_change = -sin(radians(self.dir)) * self.speed
        y_change = -cos(radians(self.dir)) * self.speed
        self.polygon.move_points(x_change, y_change)
        self.center = [self.center[0] + x_change, self.center[1] + y_change]

    def draw_bullet(self):
        self.polygon.draw(self.screen)

    def check_collision(self, entity):
        if self.polygon.points[0][0] < entity.rect.right and self.polygon.points[0][0] > entity.rect.left:
            if self.polygon.points[0][1] < entity.rect.bottom and self.polygon.points[0][1] > entity.rect.top:
                return True
        return False