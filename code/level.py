from constants import *


class Level:
    levels = {}
    current_level = 1

    def __init__(self, space, name, number, start_pos: tuple = (Screen.WIDTH / 2, Screen.HEIGHT / 2)):
        self.name = name
        self.number = number

        self.start_x, self.start_y = start_pos

        self.terrain = []

        self.background = None

        Level.levels[number] = self

    def add_terrain(self, terrain):
        self.terrain.append(terrain)

        terrain.level = self

    def draw(self, win):
        win.fill(Colors.LIGHT_GRAY3)
        for terrain in self.terrain:
            terrain.draw(win)

    @classmethod
    def get_level(cls, number) -> 'Level':
        return cls.levels[number]
