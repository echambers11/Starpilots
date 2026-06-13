from entity import Entity
from pygame import image, time

class Asteroid(Entity):
    def __init__(self, game, type, pos, angle, dir, velo, spin, hp):
        super().__init__(game, f'asteroid{type}', pos, angle, dir, velo, spin, hp)

    def _check_collisions(self):
        # check past screen
        self._return_to_screen()

        # check collisions with other entities
        if self.alive():
            for entity in self.groups()[0]:
                if entity != self and self.rect.colliderect(entity.rect) and entity.live:
                    self._handle_collision(entity)
    
    def _handle_collision(self, entity, first_call=True):        
        self._bounce(entity, first_call)
        self.take_damage()

    def _explode(self):
        self.image = image.load(f'images/{self.type}explode.png')
        self.live = False
        self.death_time = time.get_ticks() + 500
