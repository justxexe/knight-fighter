import pygame

class Player():
    test = "SUCCESS"
    def __init__(self, position):
        self.size_scale = 0.1
        self.sprite = pygame.image.load("./resources/олень.jpg")
        self.sprite = pygame.transform.scale(self.sprite,
                                                    (self.sprite.get_width() * self.size_scale,
                                                     self.sprite.get_height() * self.size_scale))
        self.velocity = 200

        self.position = list(position)
        self.hitbox = pygame.Rect(self.position[0], self.position[1], 32, 32)

        self.up_pressed = False
        self.down_pressed = False
        self.right_pressed = False
        self.left_pressed = False

    def draw(self, surface):
        pygame.draw.rect(surface, (255,0,0), self.hitbox)

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

        self.hitbox = pygame.Rect(round(self.position[0]), round(self.position[1]), 32, 32)