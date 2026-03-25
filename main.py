import pygame

from src.player import Player
from enemy import Enemy

class App:
    def __init__(self):
        self.player_sprite = None
        self._running = True
        self.screen = None
        self.size = self.weight, self.height = 1280, 720
        self.clock = pygame.time.Clock()
        self.delta_time = None
        self.enemies = []
        self.player = None
        self.background = None

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
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.player.up_pressed = False
                    if event.key == pygame.K_s:
                        self.player.down_pressed = False
                    if event.key == pygame.K_a:
                        self.player.left_pressed = False
                    if event.key == pygame.K_d:
                        self.player.right_pressed = False

            for enemy in self.enemies:
                enemy.update(self.player, self.delta_time)
                enemy.draw(self.screen)


            self.player.update(self.delta_time)
            self.player.draw(self.screen)

            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()