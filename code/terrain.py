import pygame
import pymunk
from constants import *
from characters import *


class Terrain:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.starting_x = x
        self.starting_y = y

        self.level: Level = None

    def __repr__(self) -> str:
        return f"Terrain({self.x}, {self.y}, {self.width}, {self.height})"

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def setup_physics(self):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (self.x, self.y)

        self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
        self.shape.friction = 0.5
        self.shape.elasticity = 0.5

        self.level.space.add(self.body, self.shape)

    def reset(self):
        self.x = self.starting_x
        self.y = self.starting_y

        self.setup_physics(self.level.space)

    def draw(self, win):
        pygame.draw.rect(win, Colors.DARK_GRAY3, self.rect)


class Floor(Terrain):
    def __init__(self, space, x, y, width, height):
        super().__init__(space, x, y, width, height)


class Lava(Terrain):
    def __init__(self, space, x, y, width, height):
        super().__init__(space, x, y, width, height)


class Trampoline(Terrain):
    def __init__(self, space, x, y, width, height, power):
        super().__init__(space, x, y, width, height)

        self.power = power

    def setup_physics(self, space):
        super().setup_physics(space)

        self.shape.elasticity *= self.power


class Goal(Terrain):
    def __init__(self, space, x, y, width, height, target=None):
        super().__init__(space, x, y, width, height)

        self.target = target
