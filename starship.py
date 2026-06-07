from entity import Entity
from laser import Laser

from pygame import image

class Starship(Entity):
    def __init__(self, game, type, pos, angle, dir, velo, spin, hp):
        super().__init__(game, f'starship{type}', pos, angle, dir, velo, spin, hp)
        self.accl_image = image.load(f'images/starship{type}accl.png')

    '''collisions'''
    def _check_collisions(self):
        # check collisions with other entities
        if self.alive():
            for entity in self.groups()[0]:
                if entity != self and self.rect.colliderect(entity.rect):
                    self._handle_collision(entity)
    
    def _handle_collision(self, entity, first_call=True):
        self._bounce(entity, first_call)
        self.take_damage(3)

    '''motion'''
    def turn(self, deg):
        self.spin += deg
    
    def acclerate(self, accel):
        if accel != 0:
            self._acclerate(accel)

    '''shooting'''
    def shoot(self):
        return Laser(self.screen, self.settings, self)