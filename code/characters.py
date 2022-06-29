import pygame
from level import Level
from constants import *
import os


class BaseCharacter:
    def __init__(self, pos: tuple, size: tuple, max_health=100):
        self.x, self.y = pos
        self.width, self.height = size
        self.max_health = max_health
        self.health = max_health

        self.type = None

        self.image = Fonts.CHARACTER.render("BASECHR", True, Colors.WHITE)
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))

        self.x_vel = 0
        self.y_vel = 0

        self.x_accel = 0
        self.y_accel = 0.6

        self.frame = 0

        self.queued_animations = []

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def handle_movement(self, keys, level):
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

        new.frame = self.frame

        new.queued_animations = self.queued_animations

        return new

    def _get_image(self):
        if len(self.queued_animations) > 0:
            self.image = self.queued_animations[0]
            self.queued_animations[0].frames -= 1

            if self.queued_animations[0].frames == 0:
                self.queued_animations.pop(0)

        return self.image

    def kill(self, level):
        level = Level.get_level(level)

        self.x = level.start_x
        self.y = level.start_y

        self.x_vel = 0
        self.y_vel = 0

        self.y_accel = 0.6
        self.x_accel = 0

    def draw(self, win):
        win.blit(self._get_image(), (self.x, self.y))

        self.frame += 1


class Blob(BaseCharacter):
    def __init__(self, pos: tuple, size: tuple, max_health=100):
        super().__init__(pos, size, max_health)

        self.type = CharacterType.BLOB

        self.jumping = False
        self.jump_vel = 12

        # Load images
        try:
            self.idle_image = pygame.image.load(os.path.join(
                "assets", "images", "characters", "blob", "SG Idle.png"))

            self.jumping_right_images = [pygame.image.load(os.path.join(
                "assets", "images", "characters", "blob", "Jumping", f"SG Jump {i}.png")) for i in range(1, 8)]

            self.walking_right_images = [pygame.image.load(os.path.join(
                "assets", "images", "characters", "blob", "Walking", f"SG Walk {i}.png")) for i in range(1, 4)]
        except FileNotFoundError:
            self.idle_image = pygame.image.load(os.path.join(
                "..", "assets", "images", "characters", "blob", "SG Idle.png"))

            self.jumping_right_images = [pygame.image.load(os.path.join(
                "..", "assets", "images", "characters", "blob", "Jumping", f"SG Jump {i}.png")) for i in range(1, 8)]

            self.walking_right_images = [pygame.image.load(os.path.join(
                "..", "assets", "images", "characters", "blob", "Walking", f"SG Walk {i}.png")) for i in range(1, 4)]

        self.jumping_left_images = [pygame.transform.flip(
            image, True, False) for image in self.jumping_right_images]

        self.walking_left_images = [pygame.transform.flip(
            image, True, False) for image in self.walking_right_images]

    def handle_movement(self, keys, level):
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

        self.y_vel += self.y_accel

        if abs(self.x_vel) < 5 or self.x_vel == 0 or self.x_accel == 0 or self.x_vel / abs(self.x_vel) != self.x_accel / abs(self.x_accel):
            self.x_vel += self.x_accel
        else:
            self.x_vel += -self.x_vel * 0.05

        if abs(self.x_vel) < 0.02:
            self.x_vel = 0

        self.y_accel = 0.6

        self.y_vel = round(self.y_vel, 2)
        self.x_vel = round(self.x_vel, 2)

        self.x += round(self.x_vel, 0)
        self.y += round(self.y_vel, 0)

        self.jumping = True

        self.handle_collisions(level)

    def handle_collisions(self, level):
        for terrain in Level.get_level(level).terrain:
            terrain.handle_collision(self)

    def _get_image(self):
        if self.jumping:
            if self.x_vel >= 0:
                if self.y_vel < -self.jump_vel + 1:
                    self.image = self.jumping_right_images[0]
                elif self.y_vel < -self.jump_vel + 2:
                    self.image = self.jumping_right_images[1]
                elif self.y_vel < -self.jump_vel + self.jump_vel * 0.85:
                    self.image = self.jumping_right_images[2]
                elif self.y_vel < -self.jump_vel + self.jump_vel * 1.15:
                    self.image = self.jumping_right_images[3]
                else:
                    self.image = self.jumping_right_images[4]

            elif self.x_vel < 0:
                if self.y_vel < -self.jump_vel + 1:
                    self.image = self.jumping_left_images[0]
                elif self.y_vel < -self.jump_vel + 2:
                    self.image = self.jumping_left_images[1]
                elif self.y_vel < -self.jump_vel + self.jump_vel * 0.85:
                    self.image = self.jumping_left_images[2]
                elif self.y_vel < -self.jump_vel + self.jump_vel * 1.15:
                    self.image = self.jumping_left_images[3]
                else:
                    self.image = self.jumping_left_images[4]

        else:
            rounded_frame = self.frame % 20
            if round(self.x_vel, 0) > 0:
                if rounded_frame > 15:
                    self.image = self.walking_right_images[1]
                elif rounded_frame > 10:
                    self.image = self.walking_right_images[2]
                elif rounded_frame > 5:
                    self.image = self.walking_right_images[1]
                else:
                    self.image = self.walking_right_images[0]

            elif round(self.x_vel, 0) < 0:
                if rounded_frame > 15:
                    self.image = self.walking_left_images[1]
                elif rounded_frame > 10:
                    self.image = self.walking_left_images[2]
                elif rounded_frame > 5:
                    self.image = self.walking_left_images[1]
                else:
                    self.image = self.walking_left_images[0]
            else:
                self.image = self.idle_image
                self.frame = 0

        super()._get_image()

        return self.image

    def draw(self, win):
        win.blit(self._get_image(), (self.x, self.y -
                 (self._get_image().get_height() - self.idle_image.get_height())))

        self.frame += 1


class Airplane(BaseCharacter):
    def __init__(self, pos: tuple, size: tuple, max_health=100):
        super().__init__(pos, size, max_health)

        self.type = CharacterType.AIRPLANE

        self.image = Fonts.CHARACTER.render("AIRPLANE", True, Colors.WHITE)
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))


class Spring(BaseCharacter):
    def __init__(self, pos: tuple, size: tuple, max_health=100):
        super().__init__(pos, size, max_health)

        self.type = CharacterType.SPRING

        self.image = Fonts.CHARACTER.render("SPRING", True, Colors.WHITE)
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))


class Weight(BaseCharacter):
    def __init__(self, pos: tuple, size: tuple, max_health=100):
        super().__init__(pos, size, max_health)

        self.type = CharacterType.WEIGHT

        self.image = Fonts.CHARACTER.render("WEIGHT", True, Colors.WHITE)
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))


class Plunger(BaseCharacter):
    def __init__(self, pos: tuple, size: tuple, max_health=100):
        super().__init__(pos, size, max_health)

        self.type = CharacterType.PLUNGER

        self.image = Fonts.CHARACTER.render("PLUNGER", True, Colors.WHITE)
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
