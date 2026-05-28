from entity import Entity
from math import degrees, cos, sin, radians, sqrt, atan2

class Asteroid(Entity):
    def __init__(self, game, type, pos, angle, dir, velo, spin, hp):
        super().__init__(game, f'asteroid{type}', pos, angle, dir, velo, spin, hp)

    def _check_collisions(self):
        # check past screen
        if self.pos[0] < -100:
            self.pos[0] = self.settings.screen_width + 100
        elif self.pos[0] > self.settings.screen_width + 100:
            self.pos[0] = -100
        elif self.pos[1] < -100:
            self.pos[1] = self.settings.screen_height + 100
        elif self.pos[1] > self.settings.screen_height + 100:
            self.pos[1] = -100

        # check collisions with other entities
        if self.alive():
            for entity in self.groups()[0]:
                if entity != self and self.rect.colliderect(entity.rect):
                    self._handle_collision(entity)
    
    def _handle_collision(self, entity, first_call=True):        
        self._bounce(entity, first_call)
        self.take_damage()
