import pygame

class Entity:
    def __init__(self, width, height, spritesheet):
        self.width = width
        self.height = height
        self.position = list()
        self.hitbox = list()

        self.spritesheet = spritesheet

    def draw(self, surface, animation_type, frame, is_flipped):
        image = pygame.Surface((100, 100)).convert_alpha()
        image.blit(self.spritesheet,
                   (0, 0),
                   (0 + (100 * int(frame)), 0 + (100 * animation_type), 100 + (100 * int(frame)), 100 + (100 * animation_type)))

        image = pygame.transform.scale(image, (self.width, self.height))
        image = pygame.transform.flip(image, is_flipped, False)
        image.set_colorkey((0, 0, 0))
        surface.blit(image, (self.position[0], self.position[1]))

        self.hitbox = pygame.Rect(
            self.get_center()[0] - int(self.width/20),
            self.get_center()[1] - int(self.height/10),
            int(self.width/10),
            int(self.height/5))

    def get_center(self):
        return self.position[0] + (self.width / 2), self.position[1] + (self.height / 2)







