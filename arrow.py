import pygame

class Arrow:
    def __init__(self, position, target):
        self.position = list(position)
        self.speed = 5
        self.width = 15
        self.height = 5
        self.sprite = pygame.transform.scale(pygame.image.load("./resources/arrow.png").convert(), (32, 32)).convert_alpha()

        self.hitbox = pygame.Rect(self.get_center()[0], self.get_center()[1], 25, 25)


        velocity = [position[0] - target[0], position[1] - target[1]]
        magnitude = (velocity[0] ** 2 + velocity[1] ** 2) ** 0.5

        self.velocity = [velocity[0] / magnitude * self.speed, velocity[1] / magnitude * self.speed]


    def update(self, delta):
        self.position[0] -= self.velocity[0] * delta
        self.position[1] -= self.velocity[1] * delta

    def draw(self, surface):
        surface.blit(self.sprite, self.position)
        self.hitbox = pygame.Rect(self.get_center()[0], self.get_center()[1] + 12, 16, 5)

    def get_center(self):
        return self.position[0] + (self.width / 2), self.position[1] + (self.height / 2)

