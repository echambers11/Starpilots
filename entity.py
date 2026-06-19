import pygame
from pygame.sprite import Sprite
from math import sin, cos, radians, degrees, atan2, sqrt


class Entity(Sprite):
    '''basic functions'''
    def __init__(self, game, type, pos, angle, dir, velo, spin, hp):
        super().__init__()
        # basic
        self.screen = game.screen
        self.settings = game.settings

        # sounds
        self.boom = game.boom

        # pos + velo
        self.pos = pos
        self.angle = angle
        self.dir = dir
        self.velo = velo
        self.spin = spin

        self.accl = False

        # image
        self.type = type
        self.original_image = pygame.image.load(f'images/{type}.png')
        self.init_image()
        
        # stats
        self.hp = hp
        self.live = True
        self.death_time = None

    def init_image(self):
        if self.accl:
            image = self.accl_image
        else:
            image = self.original_image
        self.image = pygame.transform.rotate(image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def draw(self):
        if not self.live:
            if pygame.time.get_ticks() > self.death_time:
                self.kill()
                return None
        self.rect.center = self.pos
        self.screen.blit(self.image, self.rect)


    '''motion'''
    def update(self):
        self._move()
        self._check_collisions()

    def _move(self):
        # spin
        if self.spin != 0:
            self.angle = (self.angle + self.spin) % 360
        
        if  self.spin != 0 or self.accl:
            self.init_image()

        # move
        x_change = -sin(radians(self.dir)) * self.velo
        y_change = -cos(radians(self.dir)) * self.velo
        self.pos[0] += x_change
        self.pos[1] += y_change

        self.rect.center = self.pos

    def _check_collisions(self):
        pass

    def _handle_collision(self, entity, first_call=True):
        pass

    def _return_to_screen(self):
        if self.pos[0] < -50:
            self.pos[0] = self.settings.screen_width + 50
        elif self.pos[0] > self.settings.screen_width + 50:
            self.pos[0] = -50
        elif self.pos[1] < -50:
            self.pos[1] = self.settings.screen_height + 50
        elif self.pos[1] > self.settings.screen_height + 50:
            self.pos[1] = -50

    def _bounce(self, entity, first_call=True):
        # Convert dir/velo to velocity vectors
        self_vx = -sin(radians(self.dir)) * self.velo
        self_vy = -cos(radians(self.dir)) * self.velo
        entity_vx = -sin(radians(entity.dir)) * entity.velo
        entity_vy = -cos(radians(entity.dir)) * entity.velo
        
        # Calculate collision normal (from self to entity)
        dx = entity.pos[0] - self.pos[0]
        dy = entity.pos[1] - self.pos[1]
        distance = sqrt(dx**2 + dy**2)
        
        # Avoid division by zero
        if distance == 0:
            distance = 1
            
        # Normalize the collision normal
        nx = dx / distance
        ny = dy / distance
        
        # Project velocities onto collision normal
        self_vel_normal = self_vx * nx + self_vy * ny
        entity_vel_normal = entity_vx * nx + entity_vy * ny
        
        # Only handle collision if objects are moving toward each other
        if self_vel_normal >= entity_vel_normal:
            # For elastic collision with equal masses: exchange normal components
            # new_self_normal = entity_vel_normal
            # new_entity_normal = self_vel_normal
            
            # Calculate new velocities after collision
            new_self_vx = self_vx + (entity_vel_normal - self_vel_normal) * nx
            new_self_vy = self_vy + (entity_vel_normal - self_vel_normal) * ny

            # bounce other entity off self
            if first_call:
                entity._handle_collision(self, False)
            
            # move out of collision range
            while self.rect.colliderect(entity.rect):
                self.pos[0] += new_self_vx
                self.pos[1] += new_self_vy
                self.rect.center = self.pos
            
            # Convert back to direction and velocity
            self.velo = sqrt(new_self_vx*new_self_vx + new_self_vy*new_self_vy)
            if self.velo > 0:
                self.dir = degrees(atan2(-new_self_vx, -new_self_vy)) % 360

    def _acclerate(self, accel):
        # Convert dir/velo to velocity vectors
        self_vx = -sin(radians(self.dir)) * self.velo
        self_vy = -cos(radians(self.dir)) * self.velo
        
        # Accelerate in the direction of the ship's current direction
        accel_vx = -sin(radians(self.angle)) * accel
        accel_vy = -cos(radians(self.angle)) * accel
        
        new_vx = self_vx + accel_vx
        new_vy = self_vy + accel_vy
        
        # Convert back to direction and velocity
        self.velo = sqrt(new_vx*new_vx + new_vy*new_vy)
        if self.velo > 0:
            self.dir = degrees(atan2(-new_vx, -new_vy)) % 360

    def take_damage(self, damage=1):
        self.hp -= damage
        if self.hp <= 0:
            self._explode()

    def _explode(self):
        self.image = pygame.image.load(f'images/explosion.png')
        self.boom.play()
        self.live = False
        self.death_time = pygame.time.get_ticks() + 500

    '''str'''
    def __str__(self):
        return f'<Entity {self.type} at {self.pos}>'