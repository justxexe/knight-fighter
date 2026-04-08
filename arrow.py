from typing import overload

import pygame
import math

from src.entity import Entity


class Arrow(Entity):
    def __init__(self, position, target):
        super().__init__(position, 15, 5, pygame.image.load("./resources/arrow.png").convert())
        self.speed = 1000
        self.target = target
        self.angle = -math.degrees(math.atan2(target[1]-position[1], target[0]-position[0]))
        sprite = pygame.transform.scale(self.spritesheet, (32, 32)).convert_alpha()
        self.sprite = pygame.transform.rotate(sprite, self.angle)

        self.hitbox = pygame.Rect(self.get_center()[0], self.get_center()[1], 25, 25)


        velocity = [position[0] - target[0], position[1] - target[1]]
        magnitude = (velocity[0] ** 2 + velocity[1] ** 2) ** 0.5

        self.velocity = [velocity[0] / magnitude * self.speed, velocity[1] / magnitude * self.speed]


    def update(self, surface, delta):
        self.position[0] -= self.velocity[0] * delta
        self.position[1] -= self.velocity[1] * delta

        self.draw(surface)


    def draw(self, surface, **kwargs):
        surface.blit(self.sprite, self.position)
        self.hitbox = pygame.Rect(self.get_center()[0], self.get_center()[1] + 12, 16, 5)

