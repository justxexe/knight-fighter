import pygame

from src.player import Player
from enemy import Enemy
from arrow import Arrow
import datetime
import random


# -132 - 118 (top-left) 1114 - 118 (rop-right) 1114 551 (bottom-right) -132 551 (bottom-left)

class App:
    def __init__(self):
        self.player_sprite = None
        self._running = True
        self.screen = None
        self.size = self.weight, self.height = 1280, 720
        self.clock = pygame.time.Clock()
        self.delta_time = None
        self.enemies = []
        self.projectiles = []
        self.player = None
        self.background = None

        self.spawn_rate = datetime.timedelta(seconds=10)
        self.last_spawn = datetime.datetime.now()
        self.spawn_points = ((-150, -120), (1150, -140), (1150, 570), (-150, 570), (-75, -120), (600, 570), (-150, 260), (540, -140))

        self.cooldown = datetime.timedelta(milliseconds=750)
        self.last_shot = datetime.datetime.now()
        # self.font = pygame.font.SysFont('Comic Sans MS', 30)

    def on_init(self):
        pygame.init()
        # pygame.font.init()
        self.screen = pygame.display.set_mode(self.size)
        self.background = pygame.image.load("./resources/background.png").convert()
        self.background = pygame.transform.scale(self.background, (1280, 720))

        self._running = True
        self.delta_time = 0.1
        self.player = Player((0, 0))
        self.enemies.append(Enemy((1000, 400)))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pygame.display.flip()
        self.delta_time = self.clock.tick(60) / 1000


    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if not self.on_init():
            self._running = True

        while self._running:
            self.screen.blit(self.background, (0,0))
            for event in pygame.event.get():
                self.on_event(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.player.up_pressed = True
                    if event.key == pygame.K_s:
                        self.player.down_pressed = True
                    if event.key == pygame.K_a:
                        self.player.left_pressed = True
                    if event.key == pygame.K_d:
                        self.player.right_pressed = True
                    if event.key == pygame.K_SPACE:
                        if datetime.datetime.now() - self.last_shot >= self.cooldown:
                            self.projectiles.append(Arrow(self.player.get_center(), pygame.mouse.get_pos()))
                            self.last_shot = datetime.datetime.now()
                            self.player.shoot()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.player.up_pressed = False
                    if event.key == pygame.K_s:
                        self.player.down_pressed = False
                    if event.key == pygame.K_a:
                        self.player.left_pressed = False
                    if event.key == pygame.K_d:
                        self.player.right_pressed = False

            for enemy in self.enemies[:]:
                enemy.update(self.screen, self.player, self.delta_time)

            for arrow in self.projectiles[:]:
                arrow.update(self.screen, self.delta_time)
                if (1114 < arrow.position[0] or arrow.position[0] < -132) or (551 < arrow.position[1] or arrow.position[1] < -118):
                    self.projectiles.remove(arrow)


            self.player.update(self.screen, self.delta_time)

            for enemy in self.enemies[:]:
                for arrow in self.projectiles[:]:
                    if enemy.hitbox.colliderect(arrow.hitbox):
                        self.enemies.remove(enemy)
                        self.projectiles.remove(arrow)
                        break
                if enemy.hitbox.colliderect(self.player.hitbox):
                    if datetime.datetime.now() - self.player.last_hit  >= datetime.timedelta(seconds=1):
                        self.player.last_hit = datetime.datetime.now()
                        self.player.take_damage(1)
                        if self.player.health <= 0:
                            self.player.die()
                            self._running = False
                            continue

            if datetime.datetime.now() - self.last_spawn >= self.spawn_rate:
                spawn_point = random.choice(self.spawn_points)
                self.enemies.append(Enemy(spawn_point))
                self.last_spawn = datetime.datetime.now()

            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()