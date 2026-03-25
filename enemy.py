import pygame

class Enemy:
    def __init__(self, position):
        self.health = 3
        self.position = list(position)
        self.speed = 100

        self.width = 50
        self.height = 50
        return

    def update(self, player, delta):
        player_position = list(player.get_center())
        position = list(self.get_center())


        velocity = [position[0] - player_position[0], position[1] - player_position[1]]
        magnitude = (velocity[0] ** 2 + velocity[1] ** 2) ** 0.5

        velocity = [velocity[0] / magnitude * self.speed, velocity[1] / magnitude * self.speed]
        print(velocity)
        self.position[0] -= velocity[0] * delta
        self.position[1] -= velocity[1] * delta

    def draw(self, surface):
        image = pygame.Surface((50, 50)).convert_alpha()
        surface.blit(image, self.position)

    def get_center(self):
        return self.position[0] + (self.width / 2), self.position[1] + (self.height / 2)
