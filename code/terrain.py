import pygame
from constants import *
from characters import *


class Terrain:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.level = None

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def check_collision(self, character: BaseCharacter):
        if not self.rect.colliderect(character.rect):
            return False

        # Left or right
        if character.rect.centery > self.y and character.rect.centery < self.y + self.height:
            if character.rect.centerx < self.rect.centerx:
                return Direction.LEFT

            elif character.rect.centerx >= self.rect.centerx:
                return Direction.RIGHT

        # Top or bottom
        elif character.x + character.width - character.width * 0.25 > self.x and character.x + character.width * 0.25 < self.x + self.width:
            if character.rect.centery < self.rect.centery:
                return Direction.UP

            elif character.rect.centery >= self.rect.centery:
                return Direction.DOWN

    def handle_collision(self, character: BaseCharacter):
        pass

    def draw(self, win):
        pygame.draw.rect(win, Colors.DARK_GRAY3, self.rect)


class Floor(Terrain):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def handle_collision(self, character: BaseCharacter):
        direction = self.check_collision(character)
        if not direction:
            return

        if character.type == CharacterType.BLOB:
            if direction == Direction.UP:
                character.y_vel = 0
                character.y_accel = 0
                character.jumping = False
                character.bounced = False
                character.y = self.rect.y - character.rect.height + 1

            elif direction == Direction.LEFT:
                character.x_vel = 0
                character.x_accel = 0
                character.x = self.rect.x - character.rect.width + 1

            elif direction == Direction.RIGHT:
                character.x_vel = 0
                character.x_accel = 0
                character.x = self.rect.x + self.rect.width - 1

            if direction == Direction.DOWN:
                character.y_vel = 0
                character.y = self.rect.y + self.rect.height

        elif character.type == CharacterType.AIRPLANE:
            if direction == Direction.UP:
                character.y_vel = 0
                character.friction = 0.05
                character.y = self.rect.y - character.rect.height + 1

            elif direction == Direction.LEFT:
                character.x_vel = 0
                character.x = self.rect.x - character.rect.width + 1

            elif direction == Direction.RIGHT:
                character.x_vel = 0
                character.x = self.rect.x + self.rect.width - 1

            if direction == Direction.DOWN:
                character.y_vel = 0
                character.y = self.rect.y + self.rect.height


class Lava(Terrain):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def handle_collision(self, character: BaseCharacter):
        direction = self.check_collision(character)
        if not direction:
            return

        character.kill(Level.current_level)

    def draw(self, win):
        pygame.draw.rect(win, Colors.RED, self.rect)


class Trampoline(Terrain):
    def __init__(self, x, y, width, height, power):
        super().__init__(x, y, width, height)

        self.power = power

    def handle_collision(self, character: BaseCharacter):
        direction = self.check_collision(character)
        if not direction:
            return

        character.bounced = True

        if direction == Direction.UP:
            character.y_vel = -self.power

        if direction == Direction.DOWN:
            character.y_vel = self.power

        if direction == Direction.LEFT:
            character.x_vel = -self.power

        if direction == Direction.RIGHT:
            character.x_vel = self.power

    def draw(self, win):
        pygame.draw.rect(win, Colors.BLUE, self.rect)


class Goal(Terrain):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def handle_collision(self, character: BaseCharacter):
        direction = self.check_collision(character)
        if not direction:
            return

        Level.current_level += 1

        character.kill(Level.current_level)

    def draw(self, win):
        pygame.draw.rect(win, Colors.GREEN, self.rect)
