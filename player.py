import pygame
import datetime

from src.entity import Entity


class Player(Entity):
    def __init__(self, position):
        super().__init__(300, 300, pygame.image.load("./resources/knight.png").convert_alpha())

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
        self.is_flipped = False

        self.is_moving = False
        self.frame = 0


    def draw(self, surface):
        if not (self.right_pressed or self.left_pressed or self.up_pressed or self.down_pressed):
            a_type = 0
            if not self.is_moving:
                if self.frame >= 5.9:
                    self.frame = 0
                else:
                    self.frame += 0.1
            else:
                self.is_moving = False
                self.frame = 0
        else:
            a_type = 1
            if self.is_moving:
                if self.frame >= 7.9:
                    self.frame = 0
                else:
                    self.frame += 0.1
            else:
                self.is_moving = True
                self.frame = 0


        image = pygame.Surface((100, 100)).convert_alpha()
        image.blit(self.spritesheet, (0, 0), (0 + (100 * int(self.frame)), 0 + (100 * a_type), 100 + (100 * int(self.frame)), 100 + (100 * a_type)))
        image = pygame.transform.scale(image, (self.width, self.height))

        if not self.right_pressed and self.left_pressed:
            self.is_flipped = True
        elif self.right_pressed and not self.left_pressed:
            self.is_flipped = False

        image = pygame.transform.flip(image, self.is_flipped, False)
        # pygame.draw.rect(surface, (255,0,0), self.hitbox)

        # circle(surface, (255, 0, 0), self.position, 10)
        # circle(surface, (255, 0, 0), (self.position[0], self.position[1] + self.height), 10)
        # circle(surface, (255, 0, 0), (self.position[0] + self.width, self.position[1]), 10)
        # circle(surface, (255, 0, 0), (self.position[0] + self.width, self.position[1] + self.height), 10)

        image.set_colorkey((0, 0, 0))
        surface.blit(image, (self.position[0], self.position[1]))

        self.hitbox = pygame.Rect(self.get_center()[0] - 15, self.get_center()[1] - 30, 30, 60)

        # circle(surface, (255, 0, 0), self.get_center(), 10)


    def update(self, delta):
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

    def get_center(self):
        return self.position[0] + (self.width / 2), self.position[1] + (self.height / 2)

    def shoot(self):
        pass