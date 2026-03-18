import pygame

class Player():
    test = "SUCCESS"
    def __init__(self, position):
        self.size_scale = 3
        self.spritesheet = pygame.image.load("./resources/knight.png").convert_alpha()
        self.velocity = 200
        self.width = 20
        self.height = 20

        self.position = list(position)
        self.hitbox = pygame.Rect(self.position[0], self.position[1], 32, 32)

        self.up_pressed = False
        self.down_pressed = False
        self.right_pressed = False
        self.left_pressed = False

    def draw(self, surface, frame):
        image = pygame.Surface((100, 100)).convert_alpha()
        image.blit(self.spritesheet, (0, 0), (0 + (100 * frame), 0 + (100 * frame), 100 + (100 * frame), 100 + (100 * frame)))
        image = pygame.transform.scale(image, (100 * self.size_scale, 100 * self.size_scale))
        image.set_colorkey((0,0,0))

        surface.blit(image, (self.position[0], self.position[1]))


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


        self.position[0] += velX * delta
        self.position[1] += velY * delta

        self.hitbox = pygame.Rect(round(self.position[0]), round(self.position[1]), self.width, self.height)