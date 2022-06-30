import pygame
from constants import *
from characters import Blob, Airplane, Spring, Weight, Plunger
from level import Level
import levels
pygame.init()


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.WIN = pygame.display.set_mode((width, height))

    def run(self):
        self.setup()
        self.loop()

    def setup(self):
        self.character = Blob((Screen.WIDTH / 2, Screen.HEIGHT / 2), (60, 60))

        Level.current_level = 1

        self.character.x = Level.get_level(Level.current_level).start_x
        self.character.y = Level.get_level(Level.current_level).start_y

        self.clock = pygame.time.Clock()
        self.running = True

    def loop(self):
        while self.running:
            self.update()
            self.draw()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.character = self.character.transform(
                        CharacterType.BLOB)
                elif event.key == pygame.K_2:
                    self.character = self.character.transform(
                        CharacterType.AIRPLANE)
                elif event.key == pygame.K_3:
                    self.character = self.character.transform(
                        CharacterType.SPRING)
                elif event.key == pygame.K_4:
                    self.character = self.character.transform(
                        CharacterType.WEIGHT)
                elif event.key == pygame.K_5:
                    self.character = self.character.transform(
                        CharacterType.PLUNGER)

                if event.key == pygame.K_r:
                    self.character.kill(Level.current_level)

            if event.type == Events.CHARACTER_DIE:
                self.character = self.character.transform(CharacterType.BLOB)

        self.character.handle_movement(
            pygame.key.get_pressed(), Level.current_level)

    def draw(self):
        self.WIN.fill(Colors.BLACK)

        Level.get_level(Level.current_level).draw(self.WIN)

        self.character.draw(self.WIN)

        pygame.display.update()

        self.clock.tick(60)


if __name__ == '__main__':
    game = Game(Screen.WIDTH, Screen.HEIGHT)
    game.run()
