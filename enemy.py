import pygame

from src.entity import Entity


class Enemy(Entity):
    def __init__(self, position):
        super().__init__(position, 300, 300, pygame.image.load("./resources/orc.png").convert_alpha())
        self.health = 3
        self.position = list(position)
        self.speed = 100

        self.frame = 0
        self.attacking_animation = False
        self.dying_animation = False
        self.alive = True

        self.hitbox = pygame.Rect(self.get_center()[0], self.get_center()[1], 25, 25)

    def update(self, surface, player, delta):
        if self.attacking_animation:
            animation_type = 2
            self.frame += 0.1
            if self.frame > 5:
                self.attacking_animation = False
                self.frame = 0
        elif self.dying_animation:
            animation_type = 5
            self.frame += 0.1
            if self.frame > 3:
                self.alive = False
        else:
            animation_type = 1
            if self.frame > 6.9:
                self.frame = 0
            else:
                self.frame += 0.05

        player_position = list(player.get_center())
        position = list(self.get_center())

        if position[0] > player_position[0]:
            is_flipped = True
        else:
            is_flipped = False

        velocity = [position[0] - player_position[0], position[1] - player_position[1]]
        magnitude = (velocity[0] ** 2 + velocity[1] ** 2) ** 0.5

        velocity = [velocity[0] / magnitude * self.speed, velocity[1] / magnitude * self.speed]

        if not self.dying_animation:
            self.position[0] -= velocity[0] * delta
            self.position[1] -= velocity[1] * delta

        self.draw(surface, animation_type, is_flipped, self.frame)


    def attack(self):
        self.frame = 0
        self.attacking_animation = True

    def die(self):
        self.frame = 0
        self.dying_animation = True


    # def draw(self, surface):
    #     image = pygame.Surface((100, 100)).convert_alpha()
    #     image.blit(self.spritesheet, (0, 0),
    #                (0 + (100 * int(self.frame)), 100, 100 + (100 * int(self.frame)),
    #                 200))
    #     image = pygame.transform.scale(image, (self.width, self.height))
    #
    #     image = pygame.transform.flip(image, self.is_flipped, False)
    #
    #     image.set_colorkey((0, 0, 0))
    #     surface.blit(image, (self.position[0], self.position[1]))
    #
    #     self.hitbox = pygame.Rect(self.get_center()[0] - 15, self.get_center()[1] - 30, 30, 60)
