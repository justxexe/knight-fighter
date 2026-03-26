import pygame

from src.player import Player
from enemy import Enemy
from arrow import Arrow
import datetime

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
        self.spawn_rate = datetime.timedelta(seconds=1)
        self.last_spawn = datetime.datetime.now()

    def on_init(self):
        pygame.init()
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
                        self.projectiles.append(Arrow(self.player.get_center(), pygame.mouse.get_pos()))
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
                enemy.update(self.player, self.delta_time)
                enemy.draw(self.screen)

            for arrow in self.projectiles[:]:
                arrow.update(self.delta_time)
                arrow.draw(self.screen)
                if (1114 < arrow.position[0] or arrow.position[0] < -132) or (551 < arrow.position[1] or arrow.position[1] < -118):
                    self.projectiles.remove(arrow)


            self.player.update(self.delta_time)
            self.player.draw(self.screen)

            for enemy in self.enemies[:]:
                for arrow in self.projectiles[:]:
                    if enemy.hitbox.colliderect(arrow.hitbox):
                        self.enemies.remove(enemy)
                        self.projectiles.remove(arrow)
                        break
                if enemy.hitbox.colliderect(self.player.hitbox):
                    if datetime.datetime.now() - self.player.last_hit  >= datetime.timedelta(seconds=1):
                        self.player.last_hit = datetime.datetime.now()
                        self.player.health -= 1
                        if self.player.health <= 0:
                            self.player = Player((0, 0))

            if datetime.datetime.now() - self.last_spawn >= self.spawn_rate:
                self.enemies.append(Enemy((800, 200)))
                self.last_spawn = datetime.datetime.now()

            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()