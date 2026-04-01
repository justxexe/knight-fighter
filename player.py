import pygame
import datetime

from src.entity import Entity


class Player(Entity):
    def __init__(self, position):
        super().__init__(position, 300, 300, pygame.image.load("./resources/knight.png").convert_alpha())

        self.size_scale = 3
        self.size_scale = 3
        self.velocity = 200
        self.health = 3
        self.last_hit = datetime.datetime.now()

        self.position = list(position)
        self.hitbox = pygame.Rect(self.get_center()[0], self.get_center()[1], 25, 25)

        self.up_pressed = False
        self.down_pressed = False
        self.right_pressed = False
        self.left_pressed = False

        self.damage_animation = False
        self.death_animation = False
        self.shooting_animation = False
        self.is_moving = False
        self.frame = 0


    def update(self, surface, delta):
        velX = 0
        velY = 0

        if self.up_pressed and not self.down_pressed:
            velY -= self.velocity
        if self.down_pressed and not self.up_pressed:
            velY += self.velocity
        if self.right_pressed and not self.left_pressed:
            velX += self.velocity
        if self.left_pressed and not self.right_pressed:
            velX -= self.velocity

        if velX != 0 and velY != 0:
            velX = velX * 0.707
            velY = velY * 0.707

        if - 132 < self.position[0] + (velX * delta) < 1114:
            self.position[0] += velX * delta
        if -118 < self.position[1] + (velY * delta) < 551:
            self.position[1] += velY * delta

        self.hitbox = pygame.Rect(round(self.position[0]), round(self.position[1]), self.width, self.height)
        # -132 - 118 (top-left) 1114 - 118 (rop-right) 1114 551 (bottom-right) -132 551 (bottom-left)

        # установка animation_type и frame; анимация
        if self.death_animation:
            animation_type = 6
            self.frame += 0.1
            if self.frame > 3:
                return False
        elif self.damage_animation:
            animation_type = 5
            self.frame += 0.1
            if self.frame > 3:
                self.frame = 0
                self.damage_animation = False
        elif self.shooting_animation:
            self.frame += 0.5
            animation_type = 4
            if self.frame > 8:
                self.frame = 0
                self.shooting_animation = False
        elif not (self.right_pressed or self.left_pressed or self.up_pressed or self.down_pressed):
            animation_type = 0
            if not self.is_moving:
                if self.frame >= 5.9:
                    self.frame = 0
                else:
                    self.frame += 0.1
            else:
                self.is_moving = False
                self.frame = 0
        else:
            animation_type = 1
            if self.is_moving:
                if self.frame >= 7.9:
                    self.frame = 0
                else:
                    self.frame += 0.1
            else:
                self.is_moving = True
                self.frame = 0

        if not self.right_pressed and self.left_pressed:
            is_flipped = True
        else:
            is_flipped = False

        self.draw(surface, animation_type, is_flipped, self.frame)
        return None

    def die(self):
        self.frame = 0
        self.death_animation = True

    def take_damage(self, damage):
        self.health -= damage
        self.frame = 0
        self.damage_animation = True

    def shoot(self):
        self.frame = 0
        self.shooting_animation = True