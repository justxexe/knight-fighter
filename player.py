import pygame

class Player:
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
        image = pygame.transform.scale(image, (100 * self.size_scale, 100 * self.size_scale))

        if not self.right_pressed and self.left_pressed:
            self.is_flipped = True
        elif self.right_pressed and not self.left_pressed:
            self.is_flipped = False

        image = pygame.transform.flip(image, self.is_flipped, False)

        image.set_colorkey((0, 0, 0))
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