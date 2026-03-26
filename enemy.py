import pygame

class Enemy:
    def __init__(self, position):
        self.health = 3
        self.position = list(position)
        self.speed = 100

        self.width = 300
        self.height = 300

        self.spritesheet = pygame.image.load("./resources/orc.png").convert_alpha()
        self.frame = 0
        self.is_flipped = False

        self.hitbox = pygame.Rect(self.get_center()[0], self.get_center()[1], 25, 25)

    def update(self, player, delta):

        if self.frame > 7.9:
            self.frame = 0
        else:
            self.frame += 0.05
        player_position = list(player.get_center())
        position = list(self.get_center())

        if position[0] > player_position[0]:
            self.is_flipped = True
        else:
            self.is_flipped = False

        velocity = [position[0] - player_position[0], position[1] - player_position[1]]
        magnitude = (velocity[0] ** 2 + velocity[1] ** 2) ** 0.5

        velocity = [velocity[0] / magnitude * self.speed, velocity[1] / magnitude * self.speed]

        self.position[0] -= velocity[0] * delta
        self.position[1] -= velocity[1] * delta

    def draw(self, surface):
        image = pygame.Surface((100, 100)).convert_alpha()
        image.blit(self.spritesheet, (0, 0),
                   (0 + (100 * int(self.frame)), 100, 100 + (100 * int(self.frame)),
                    200))
        image = pygame.transform.scale(image, (self.width, self.height))

        image = pygame.transform.flip(image, self.is_flipped, False)

        image.set_colorkey((0, 0, 0))
        surface.blit(image, (self.position[0], self.position[1]))

        self.hitbox = pygame.Rect(self.get_center()[0] - 15, self.get_center()[1] - 30, 30, 60)

    def get_center(self):
        return self.position[0] + (self.width / 2), self.position[1] + (self.height / 2)
