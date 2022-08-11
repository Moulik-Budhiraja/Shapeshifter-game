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

        self.character = None

    def add_terrain(self, terrain):
        self.terrain.append(terrain)

        terrain.level = self

        terrain.setup_physics(len(self.terrain) + CollisionType.CHARACTER)

    def reset(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 981)

        for counter, terrain in enumerate(self.terrain):
            terrain.reset(counter + CollisionType.CHARACTER + 1)

    def init_terrain(self):
        for counter, terrain in enumerate(self.terrain):
            terrain.setup_physics(counter + CollisionType.CHARACTER + 1)

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
