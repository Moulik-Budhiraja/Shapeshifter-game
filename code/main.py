import pygame
pygame.init()

WIDTH = 1120
HEIGHT = 630

WIN = pygame.display.set_mode((WIDTH, HEIGHT))


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def run(self):
        self.setup()
        self.loop()

    def setup(self):

        self.running = True

    def loop(self):
        while self.running():
            self.update()
            self.draw()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def draw(self):
        WIN.fill((0, 0, 0))
        pygame.display.update()
