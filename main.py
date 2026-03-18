import pygame

from src.player import Player

class App:
    def __init__(self):
        self.player_sprite = None
        self._running = True
        self.screen = None
        self.size = self.weight, self.height = 300, 500
        self.clock = pygame.time.Clock()
        self.delta_time = None
        self.entities = []

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)

        self._running = True
        self.delta_time = 0.1
        self.entities.append(Player((0, 0)))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pygame.display.flip()
        self.delta_time = self.clock.tick(120) / 1000


    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if not self.on_init():
            self._running = True


        while self._running:
            self.screen.fill((20, 20, 20))
            for event in pygame.event.get():
                self.on_event(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.entities[0].up_pressed = True
                    if event.key == pygame.K_s:
                        self.entities[0].down_pressed = True
                    if event.key == pygame.K_a:
                        self.entities[0].left_pressed = True
                    if event.key == pygame.K_d:
                        self.entities[0].right_pressed = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.entities[0].up_pressed = False
                    if event.key == pygame.K_s:
                        self.entities[0].down_pressed = False
                    if event.key == pygame.K_a:
                        self.entities[0].left_pressed = False
                    if event.key == pygame.K_d:
                        self.entities[0].right_pressed = False

            self.entities[0].update(self.delta_time)

            for entity in self.entities:
                entity.draw(self.screen, 0)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()