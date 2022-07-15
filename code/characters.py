import pygame
from level import Level
from constants import *
from animations import Animation
import math
import os

show_hitboxes = True


class BaseCharacter:
    def __init__(self, pos: tuple, size: tuple, max_health=100):
        self.x, self.y = pos
        self.width, self.height = size
        self.max_health = max_health
        self.health = max_health

        self.x_offset = 0
        self.y_offset = 0

        self.type = None

        self.image = Fonts.CHARACTER.render("BASECHR", True, Colors.WHITE)
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))

        self.x_vel = 0
        self.y_vel = 0

        self.x_accel = 0
        self.y_accel = Motion.GRAVITY

        self.frame = 0

        self.queued_animations = []

        self.transform_animations_right = []
        self.transform_animations_left = []

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width - self.x_offset, self.height - self.y_offset)

    def handle_movement(self, keys, level):
        pass

    def transform(self, type: CharacterType):
        if self.type == type:
            return self

        if type == CharacterType.BLOB:
            new = Blob((self.x, self.y - self.y_offset), (self.width,
                       self.height), self.max_health)
            new.jumping = True
        elif type == CharacterType.AIRPLANE:
            new = Airplane((self.x, self.y - self.y_offset), (self.width,
                                                              self.height), self.max_health)
        elif type == CharacterType.SPRING:
            new = Spring((self.x, self.y - self.y_offset), (self.width,
                                                            self.height), self.max_health)
        elif type == CharacterType.WEIGHT:
            new = Weight((self.x, self.y - self.y_offset), (self.width,
                                                            self.height), self.max_health)
        elif type == CharacterType.PLUNGER:
            new = Plunger((self.x, self.y - self.y_offset), (self.width,
                                                             self.height), self.max_health)

        new.y += new.y_offset

        new.health = self.health

        new.x_vel = self.x_vel
        new.y_vel = self.y_vel

        new.x_accel = self.x_accel
        new.y_accel = self.y_accel

        new.frame = self.frame

        new.queued_animations = self.queued_animations

        if self.x_vel >= 0:
            new.queued_animations += reversed([a.copy()
                                              for a in self.transform_animations_right])
            new.queued_animations += [a.copy()
                                      for a in new.transform_animations_right]
        else:
            new.queued_animations += reversed([a.copy()
                                              for a in self.transform_animations_left])
            new.queued_animations += [a.copy()
                                      for a in new.transform_animations_left]

        return new

    def _get_image(self):
        if len(self.queued_animations) > 0:
            self.image = self.queued_animations[0].image
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

        self.y_accel = Motion.GRAVITY
        self.x_accel = 0

        pygame.event.post(pygame.event.Event(Events.CHARACTER_DIE))

    def draw(self, win):
        win.blit(self._get_image(), (self.x, self.y))

        self.frame += 1


class Blob(BaseCharacter):
    def __init__(self, pos: tuple, size: tuple, max_health=100):
        super().__init__(pos, size, max_health)

        self.type = CharacterType.BLOB

        self.jumping = False
        self.jump_vel = 12

        self.mass = 1

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
            self.x_accel = -self.x_vel * 0.05 * self.mass

            if not self.jumping:
                self.x_accel = -self.x_vel * 0.2 * self.mass

        elif keys[pygame.K_LEFT]:
            self.x_accel = -2.5
        elif keys[pygame.K_RIGHT]:
            self.x_accel = 2.5

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

        if show_hitboxes:
            pygame.draw.rect(win, Colors.RED, self.rect, 1)

        self.frame += 1


class Airplane(BaseCharacter):
    def __init__(self, pos: tuple, size: tuple, max_health=100):
        super().__init__(pos, size, max_health)

        self.type = CharacterType.AIRPLANE

        self.mass = 0.15
        self.drag = 0.01
        self.friction = 0

        self.turn_speed = 3

        self.y_offset = 30

        try:
            self.image_up_right = pygame.image.load(os.path.join(
                "assets", "images", "characters", "plane", "SG Plane Up.png"))
            self.image_down_right = pygame.image.load(os.path.join(
                "assets", "images", "characters", "plane", "SG Plane Down.png"))

            self.transform_images_right = [pygame.image.load(os.path.join(
                "assets", "images", "characters", "plane", f"SG Plane Transform {i}.png")) for i in range(1, 3)]
        except FileNotFoundError:
            self.image_up_right = pygame.image.load(os.path.join(
                "..", "assets", "images", "characters", "plane", "SG Plane Up.png"))
            self.image_down_right = pygame.image.load(os.path.join(
                "..", "assets", "images", "characters", "plane", "SG Plane Down.png"))

            self.transform_images_right = [pygame.image.load(os.path.join(
                "..", "assets", "images", "characters", "plane", f"SG Plane Transform {i}.png")) for i in range(1, 3)]

        self.image_up_left = pygame.transform.flip(
            self.image_up_right, True, False)
        self.image_down_left = pygame.transform.flip(
            self.image_down_right, True, False)
        self.transform_images_left = [pygame.transform.flip(
            image, True, False) for image in self.transform_images_right]

        self.transform_animations_right = [
            Animation(image, 3) for image in self.transform_images_right]
        self.transform_animations_left = [
            Animation(image, 3) for image in self.transform_images_left]

    @property
    def angle(self):
        return math.degrees(math.atan2(self.y_vel, self.x_vel))

    @angle.setter
    def angle(self, angle):
        self.x_vel = math.cos(math.radians(angle)) * self.velocity
        self.y_vel = math.sin(math.radians(angle)) * self.velocity

    @property
    def velocity(self):
        return math.hypot(self.x_vel, self.y_vel)

    def handle_movement(self, keys, level):
        if keys[pygame.K_UP]:
            if self.x_vel > 0:
                if self.angle - self.turn_speed > -90:
                    self.angle -= self.turn_speed
            else:
                if self.angle + self.turn_speed < -90 or self.angle > 90:
                    self.angle += self.turn_speed

        if keys[pygame.K_DOWN]:
            # print(self.angle, self.x_vel)
            if self.x_vel > 0:
                if self.angle + self.turn_speed < 90:
                    self.angle += self.turn_speed
            else:
                if self.angle - self.turn_speed > 90:
                    self.angle -= self.turn_speed

        pass

    def _get_image(self):
        # Pointing Down
        if self.angle >= 0:
            if self.x_vel >= 0:
                self.image = self.image_up_right
            elif self.x_vel < 0:
                self.image = self.image_up_left
        else:
            if self.x_vel >= 0:
                self.image = self.image_up_right
            elif self.x_vel < 0:
                self.image = self.image_up_left

        super()._get_image()

        if self.angle >= 0:
            if self.x_vel >= 0:
                self.image = pygame.transform.rotate(self.image, -self.angle)
            elif self.x_vel < 0:
                self.image = pygame.transform.rotate(
                    self.image, -self.angle + 180)
        else:
            if self.x_vel >= 0:
                self.image = pygame.transform.rotate(self.image, -self.angle)
            elif self.x_vel < 0:
                self.image = pygame.transform.rotate(
                    self.image, -self.angle + 180)

        return self.image

    def draw(self, win):
        win.blit(self._get_image(), (self.x, self.y))

        if show_hitboxes:
            pygame.draw.rect(win, Colors.RED, self.rect, 1)

        self.frame += 1


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

        self.x_offset = 38
        self.y_offset = 38

        self.mass = 3

        self.friction = 0.001

        try:
            self.image_ball = pygame.image.load(os.path.join(
                "assets", "images", "characters", "metal ball", "SG Ball.png"))

            self.transform_images = [pygame.image.load(os.path.join(
                "assets", "images", "characters", "metal ball", f"SG Ball Transform {i}.png")) for i in range(1, 3)]

        except FileNotFoundError:
            self.image_ball = pygame.image.load(os.path.join(
                "..", "assets", "images", "characters", "metal ball", "SG Ball.png"))

            self.transform_images = [pygame.image.load(os.path.join(
                "..", "assets", "images", "characters", "metal ball", f"SG Ball Transform {i}.png")) for i in range(1, 3)]

        self.transform_animations_right = [
            Animation(image, 3) for image in self.transform_images]
        self.transform_animations_left = [
            Animation(image, 3) for image in self.transform_images]

    def handle_movement(self, keys, level):
        pass

    def draw(self, win):
        win.blit(self._get_image(), (self.x, self.y))

        if show_hitboxes:
            pygame.draw.rect(win, Colors.RED, self.rect, 1)

        self.frame += 1


class Plunger(BaseCharacter):
    def __init__(self, pos: tuple, size: tuple, max_health=100):
        super().__init__(pos, size, max_health)

        self.type = CharacterType.PLUNGER

        self.image = Fonts.CHARACTER.render("PLUNGER", True, Colors.WHITE)
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
