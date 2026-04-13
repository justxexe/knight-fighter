import pygame

from src.player import Player
from enemy import Enemy
from arrow import Arrow
import datetime
import random


# -132 - 118 (top-left) 1114 - 118 (top-right) 1114 551 (bottom-right) -132 551 (bottom-left)

class KnightFighter:
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
        self.score = 0

        self.spawn_rate = datetime.timedelta(milliseconds=900)
        self.last_spawn = datetime.datetime.now()
        self.spawn_points = ((-150, -120), (1150, -140), (1150, 570), (-150, 570), (-75, -120), (600, 570), (-150, 260), (540, -140))

        self.cooldown = datetime.timedelta(milliseconds=750)
        self.last_shot = datetime.datetime.now()

        self.font = None

    def on_init(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 30, bold=True)

        self.screen = pygame.display.set_mode(self.size)
        self.background = pygame.image.load("./resources/background.png").convert()
        self.background = pygame.transform.scale(self.background, (1280, 720))

        self._running = True
        self.delta_time = 0.1

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pygame.display.flip()

        self.delta_time = self.clock.tick(60) / 1000

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if not self.on_init():
            self._running = True

        while self._running:
            self.screen.blit(self.background, (0,0))
            if not self.player:
                menu_text = self.font.render("Для начала игры нажмите пробел", (0,0,0), 5)
                self.screen.blit(menu_text, (380, 250))
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.player = Player((0,0))
                self.on_loop()
            elif self.player.alive:
                for event in pygame.event.get():
                    self.on_event(event)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_i or event.key == pygame.K_w:
                            self.player.up_pressed = True
                        if event.key == pygame.K_k or  event.key == pygame.K_s:
                            self.player.down_pressed = True
                        if event.key == pygame.K_j or  event.key == pygame.K_a:
                            self.player.left_pressed = True
                        if event.key == pygame.K_l or  event.key == pygame.K_d:
                            self.player.right_pressed = True
                        if event.key == pygame.K_SPACE:
                            if datetime.datetime.now() - self.last_shot >= self.cooldown:
                                self.projectiles.append(Arrow(self.player.get_center(), pygame.mouse.get_pos()))
                                self.last_shot = datetime.datetime.now()
                                self.player.shoot()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_i or  event.key == pygame.K_w:
                            self.player.up_pressed = False
                        if event.key == pygame.K_k or  event.key == pygame.K_s:
                            self.player.down_pressed = False
                        if event.key == pygame.K_j or  event.key == pygame.K_a:
                            self.player.left_pressed = False
                        if event.key == pygame.K_l or  event.key == pygame.K_d:
                            self.player.right_pressed = False

                for enemy in self.enemies[:]:
                    enemy.update(self.screen, self.player, self.delta_time)

                for arrow in self.projectiles[:]:
                    arrow.update(self.screen, self.delta_time)
                    if (1280 < arrow.get_center()[0] or arrow.get_center()[0] < 0) or (720 < arrow.get_center()[1] or arrow.get_center()[1] < 0):
                        self.projectiles.remove(arrow)


                self.player.update(self.screen, self.delta_time)

                for enemy in self.enemies[:]:
                    if enemy.just_attacked:
                        self.player.take_damage(1)
                        if self.player.health <= 0:
                            self.player.die()
                    if not enemy.alive:
                        self.enemies.remove(enemy)
                        continue
                    for arrow in self.projectiles[:]:
                        if enemy.hitbox.colliderect(arrow.hitbox):
                            enemy.die()
                            self.projectiles.remove(arrow)
                            self.score += 1
                            break

                    if enemy.hitbox.colliderect(self.player.hitbox):
                        if datetime.datetime.now() - self.player.last_hit  >= datetime.timedelta(seconds=1):
                            self.player.last_hit = datetime.datetime.now()
                            enemy.attack()

                if datetime.datetime.now() - self.last_spawn >= self.spawn_rate:
                    spawn_point = random.choice(self.spawn_points)
                    self.enemies.append(Enemy(spawn_point))
                    self.last_spawn = datetime.datetime.now()

                score_text = self.font.render('очки', 1, (210, 0, 0))
                self.screen.blit(score_text, (600, 0))
                score_text = self.font.render(str(self.score), 1, (210, 0, 0))
                self.screen.blit(score_text, (630, 30))
                healthbar_red = pygame.rect.Rect(self.player.get_center()[0] - 20, self.player.get_center()[1] - 45, 40, 6)
                healthbar_green = pygame.rect.Rect(self.player.get_center()[0] - 20,
                                                   self.player.get_center()[1] - 45,
                                                   self.player.health * (40/3),
                                                   6)

                pygame.draw.rect(self.screen, (255,0,0), healthbar_red)
                pygame.draw.rect(self.screen, (0,255,0), healthbar_green)

                self.on_loop()
            else:
                self.screen.fill((0,0,0))
                self.screen.blit(self.background, (0, 0))
                background = pygame.transform.average_color(self.background)
                game_over_text = self.font.render("ИГРА ОКОНЧЕНА", (210, 10, 0),5)
                death_text = self.font.render("Вы умерли", (200, 20, 0), 4)
                score_text = self.font.render(f"Ваш финальный счет: {self.score}", (200, 20, 0), 4)
                quit_text = self.font.render("Нажмите Q что бы выйти", (200, 20, 0), 4)
                self.screen.blit(game_over_text, (500, 250))
                self.screen.blit(death_text, (540, 290))
                self.screen.blit(score_text, (450, 340))
                self.screen.blit(quit_text, (450, 370))
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self._running = False
                self.on_loop()
        self.on_cleanup()


if __name__ == "__main__":
    knight_fighter = KnightFighter()
    knight_fighter.on_execute()