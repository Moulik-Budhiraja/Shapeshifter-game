import pygame
import pymunk
from level import Level
from constants import *
from animations import Animation
from movement import MovementHandler


class Character:
    TYPES = {
        CharacterType.BLOB: {
            "movement": MovementHandler.standard,
        },
        CharacterType.AIRPLANE: {
        },
        CharacterType.SPRING: {
        },
        CharacterType.WEIGHT: {
        },
        CharacterType.PLUNGER: {
        },
    }

    def __init__(self):
        self.transform(CharacterType.BLOB)

    def transform(self, character_type):
        self.character_type = character_type

    def set_level(self, level):
        self.level = level

        # Reset level and add self to level space

    def move(self, keys)


class BaseCharacter:
    def __init__(self, space, pos: tuple, size: tuple):
        self.space = space
        self.x, self.y = pos
        self.width, self.height = size

        self.type = None

        self.image = Fonts.CHARACTER.render("BASECHR", True, Colors.WHITE)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.setup_physics()

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def setup_physics(self):
        pass

    def transform(self, type: CharacterType):
        if self.type == type:
            return self

        if type == CharacterType.BLOB:
            new = Blob(self.space, (self.x, self.y), (self.width, self.height))
        elif type == CharacterType.AIRPLANE:
            new = Airplane(self.space, (self.x, self.y), (self.width, self.height))
        elif type == CharacterType.SPRING:
            new = Spring(self.space, (self.x, self.y), (self.width, self.height))
        elif type == CharacterType.WEIGHT:
            new = Weight(self.space, (self.x, self.y), (self.width, self.height))
        elif type == CharacterType.PLUNGER:
            new = Plunger(self.space, (self.x, self.y), (self.width, self.height))

        return new

    def handle_movement(self, keys, level):
        pass

    def _get_image(self):
        return self.image

    def kill(self, level):
        pass

    def draw(self, win):
        win.blit(self._get_image(), (self.x, self.y))


class Blob(BaseCharacter):
    def __init__(self, space, pos: tuple, size: tuple):
        super().__init__(space, pos, size)

        self.image = Fonts.CHARACTER.render("BLOB", True, Colors.WHITE)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def setup_physics(self):
        self.body = pymunk.Body()
        self.body.position = self.x, self.y
        self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
        self.shape.mass = 1
        self.shape.friction = 0.5
        self.shape.elasticity = 0.1

        self.space.add(self.body, self.shape)

    def handle_movement(self, keys, level):
        if keys[pygame.K_LEFT]:
            self.body.apply_impulse_at_local_point((-1000, 0))
        if keys[pygame.K_RIGHT]:
            self.body.apply_impulse_at_local_point((1000, 0))
        if keys[pygame.K_UP]:
            self.body.apply_impulse_at_local_point((0, -1000))


class Airplane(BaseCharacter):
    def __init__(self, space, pos: tuple, size: tuple):
        super().__init__(space, pos, size)

        self.type = CharacterType.AIRPLANE

        self.image = Fonts.CHARACTER.render("PLANE", True, Colors.WHITE)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


class Spring(BaseCharacter):
    def __init__(self, space, pos: tuple, size: tuple):
        super().__init__(space, pos, size)

        self.type = CharacterType.SPRING

        self.image = Fonts.CHARACTER.render("SPRING", True, Colors.WHITE)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


class Weight(BaseCharacter):
    def __init__(self, space, pos: tuple, size: tuple):
        super().__init__(space, pos, size)

        self.image = Fonts.CHARACTER.render("WEIGHT", True, Colors.WHITE)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.type = CharacterType.WEIGHT


class Plunger(BaseCharacter):
    def __init__(self, space, pos: tuple, size: tuple):
        super().__init__(space, pos, size)

        self.type = CharacterType.PLUNGER

        self.image = Fonts.CHARACTER.render("PLUNGER", True, Colors.WHITE)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
