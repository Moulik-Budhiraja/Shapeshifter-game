from lib2to3.pytree import Base
import pygame
from constants import *


class BaseCharacter:
    def __init__(self, pos: tuple, size: tuple, max_health=100):
        self.x, self.y = pos
        self.width, self.height = size
        self.max_health = max_health
        self.health = max_health

        self.image = Fonts.CHARACTER.render("BASECHR", True, Colors.WHITE)
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))

        self.x_vel = 0
        self.y_vel = 0

        self.x_accel = 0
        self.y_accel = 0

    def handle_movement(self, keys):
        pass

    def transform(self, type: CharacterType):
        if type == CharacterType.BLOB:
            new = Blob((self.x, self.y), (self.width,
                       self.height), self.max_health)
        elif type == CharacterType.AIRPLANE:
            new = Airplane((self.x, self.y), (self.width,
                           self.height), self.max_health)
        elif type == CharacterType.SPRING:
            new = Spring((self.x, self.y), (self.width,
                         self.height), self.max_health)
        elif type == CharacterType.WEIGHT:
            new = Weight((self.x, self.y), (self.width,
                         self.height), self.max_health)
        elif type == CharacterType.PLUNGER:
            new = Plunger((self.x, self.y), (self.width,
                          self.height), self.max_health)

        new.health = self.health

        new.x_vel = self.x_vel
        new.y_vel = self.y_vel

        new.x_accel = self.x_accel
        new.y_accel = self.y_accel

        return new

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class Blob(BaseCharacter):
    def __init__(self, pos: tuple, size: tuple, max_health=100):
        super().__init__(pos, size, max_health)
        self.image = Fonts.CHARACTER.render("BLOB", True, Colors.WHITE)
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))

        self.jumping = False
        self.jump_vel = 12

    def handle_movement(self, keys):
        if keys[pygame.K_LEFT] == keys[pygame.K_RIGHT]:
            self.x_accel = -self.x_vel * 0.05

            if not self.jumping:
                self.x_accel = -self.x_vel * 0.2

        elif keys[pygame.K_LEFT]:
            self.x_accel = -2.5
        elif keys[pygame.K_RIGHT]:
            self.x_accel = 2.5

        if keys[pygame.K_UP]:
            if not self.jumping:
                self.jumping = True
                self.y_vel = -self.jump_vel

        # If not colliding with terrain

        if self.jumping:
            self.y_accel = 0.8
        else:
            self.y_accel = 0

        self.y_vel += self.y_accel
        self.x_vel += self.x_accel

        if self.x_vel > 5:
            self.x_vel = 5
        elif self.x_vel < -5:
            self.x_vel = -5

        self.y_vel = round(self.y_vel, 1)

        if self.y_vel == self.jump_vel:
            self.jumping = False
            self.y_vel = 0

        self.x += round(self.x_vel)
        self.y += self.y_vel


class Airplane(BaseCharacter):
    def __init__(self, pos: tuple, size: tuple, max_health=100):
        super().__init__(pos, size, max_health)
        self.image = Fonts.CHARACTER.render("AIRPLANE", True, Colors.WHITE)
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))


class Spring(BaseCharacter):
    def __init__(self, pos: tuple, size: tuple, max_health=100):
        super().__init__(pos, size, max_health)
        self.image = Fonts.CHARACTER.render("SPRING", True, Colors.WHITE)
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))


class Weight(BaseCharacter):
    def __init__(self, pos: tuple, size: tuple, max_health=100):
        super().__init__(pos, size, max_health)
        self.image = Fonts.CHARACTER.render("WEIGHT", True, Colors.WHITE)
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))


class Plunger(BaseCharacter):
    def __init__(self, pos: tuple, size: tuple, max_health=100):
        super().__init__(pos, size, max_health)
        self.image = Fonts.CHARACTER.render("PLUNGER", True, Colors.WHITE)
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
