import pygame
import pymunk
import pymunk.pygame_util
import matplotlib.path as mplpath
from constants import *
from characters import Blob, Airplane, Spring, Weight, Plunger
from level import Level
import levels
pygame.init()
import os


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.WIN = pygame.display.set_mode((width, height))

    def run(self):
        self.setup()
        self.loop()

    def setup(self):
        self.FPS = 60
        self.DT = 1 / self.FPS
        self.SUB_STEPS = 10
        self.clock = pygame.time.Clock()



        self.draw_options = pymunk.pygame_util.DrawOptions(self.WIN)

        Level.current_level = 5

        levels.generate_levels()

        self.character = Blob(Level.get_current_level().space, (
            Screen.WIDTH / 2, Screen.HEIGHT / 2), (60, 60))
        
        self.character.x = Level.get_level(Level.current_level).start_x
        self.character.y = Level.get_level(Level.current_level).start_y

        self.character.setup_physics()

        self.running = True

        os.system("clear")
        self.line_counter = 0
        



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
                    self.character.set_level(Level.get_current_level())

                if event.key == pygame.K_h:
                    self.character.show_hitbox = not self.character.show_hitbox
                if event.key == pygame.K_SPACE:
                    print(f"\r{self.line_counter}. {pygame.mouse.get_pos()}")
                    self.line_counter += 1

                if event.key == pygame.K_c:
                    os.system("clear")
                    self.line_counter = 0

            if event.type == Events.CHARACTER_DIE:
                self.character = self.character.transform(CharacterType.BLOB)

        self.character.handle_movement(
            pygame.key.get_pressed())

        if self.character.show_hitbox:
            terrains = []
            mouse = pygame.mouse.get_pos()
            for terrain in Level.get_current_level().terrain:
                path = mplpath.Path(terrain.polygon)
                if path.contains_point(mouse):
                    terrains.append(terrain)

            print(" " * 150, end="\r")
            print(pygame.mouse.get_pos(), [i for i in terrains], sep=" | ", end="\r")

        for _ in range(self.SUB_STEPS):
            Level.get_level(Level.current_level).space.step(self.DT / self.SUB_STEPS)
            self.character.velocity_adjustments()

        self.character.update_location()

    def draw(self):
        self.WIN.fill(Colors.BLACK)

        Level.get_level(Level.current_level).draw(self.WIN)

        # Level.get_level(Level.current_level).space.debug_draw(self.draw_options)

        self.character.draw(self.WIN)

        pygame.display.update()

        self.clock.tick(self.FPS)


if __name__ == '__main__':
    game = Game(Screen.WIDTH, Screen.HEIGHT)
    game.run()
