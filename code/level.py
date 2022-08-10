from constants import *
import helpers
import pymunk


class Level:
    levels = {}
    current_level = 1

    def __init__(self, name, number, start_pos: tuple = (Screen.WIDTH / 2, Screen.HEIGHT / 2)):
        self.name = name
        self.number = number
        Level.levels[number] = self

        self.space = pymunk.Space()
        self.space.gravity = (0, 981)

        self.start_x, self.start_y = start_pos

        self.terrain = []

        self.background = None

    def add_terrain(self, terrain):
        self.terrain.append(terrain)

        terrain.level = self

        terrain.setup_physics()

    def reset(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 981)

        for terrain in self.terrain:
            terrain.reset(self.space)

    def draw(self, win):
        win.fill(Colors.LIGHT_GRAY3)
        for terrain in self.terrain:
            terrain.draw(win)

    @classmethod
    def get_level(cls, number) -> 'Level':
        return cls.levels[number]

    @classmethod
    def get_current_level(cls) -> 'Level':
        return cls.levels[cls.current_level]
