from starship import Starship
from pygame import time
from math import atan2, degrees

class Enemy(Starship):
    def __init__(self, game, type, pos, angle, dir, velo, spin, hp):
        super().__init__(game, type, pos, angle, dir, velo, spin, hp)
        self.target = game.p1

    '''collisions'''
    def _check_collisions(self):
        # check past screen
        self._return_to_screen()
        
        # check collisions with other entities
        if self.alive():
            for entity in self.groups()[0]:
                if entity != self and self.rect.colliderect(entity.rect):
                    self._handle_collision(entity)
    
    def _handle_collision(self, entity, first_call=True):
        self._bounce(entity, first_call)
        self.take_damage(3)
    
    '''motion'''
    def update(self):
        self.accl = False
        if time.get_ticks() > 3000:
            self._aim()
            self._approach()
            self._attack()
        self._move()
        self._check_collisions()

    def _aim(self):
        # aim at player
        angle_diff = self._get_angle_diff()
        
        # check if not spinning enough or spinning the wrong way, then turn
        if angle_diff != 0:
            if abs(angle_diff) > abs(self.spin*10) or angle_diff/abs(angle_diff) != self.spin/abs(self.spin):
                if angle_diff < 0:
                    self.turn(-self.settings.ship_turn)
                elif angle_diff > 0:
                    self.turn(self.settings.ship_turn)
            # otherwise, decelerate to stop spinning
            else:
                if angle_diff < 0:
                    self.turn(self.settings.ship_turn)
                elif angle_diff > 0:
                    self.turn(-self.settings.ship_turn)

    def _attack(self):
        angle_diff = self._get_angle_diff()
        # shoot if aimed at player
        if abs(angle_diff) < 10:
            self.attack_timer += 1
            self.shoot()

    def _approach(self):
        # move towards player if not too close
        y_to_target = self.target.pos[1] - self.pos[1]
        x_to_target = self.target.pos[0] - self.pos[0]
        distance = (y_to_target**2 + x_to_target**2)**0.5
        if (distance > 150 and self.velo < self.settings.enemy_max_speed) or abs(self.dir - self.angle) > 90:
            self.acclerate(self.settings.ship_accel)
            self.accl = True
            
    def _get_angle_diff(self):
        y_to_target = self.target.pos[1] - self.pos[1]
        x_to_target = self.target.pos[0] - self.pos[0]
        target_angle = -(degrees(atan2(y_to_target, x_to_target)) - 90) % 360
        angle_diff = (target_angle - self.angle) % 360 - 180
        return angle_diff