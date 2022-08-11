import pygame
import pymunk
from level import Level
from constants import *
from animations import Animation
import helpers
import math

class BaseCharacter:
    def __init__(self, space, pos: tuple, size: tuple):
        self.space = space
        self.x, self.y = pos
        self.original_width, self.original_height = size
        self.width, self.height = size

        self.type = None

        self.image = Fonts.CHARACTER.render("BASECHR", True, Colors.WHITE)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.setup_physics()

        self.init_level(Level.get_current_level())

        self.show_hitbox = False

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def setup_physics(self):
        pass

    def post_transform(self):
        pass

    def set_level(self, level: Level):
        level.reset()

        self.space = level.space

        self.x = level.start_x
        self.y = level.start_y

        level.character = self

        self.setup_physics()

    def init_level(self, level: Level):
        self.space = level.space

        level.init_terrain()

        level.character = self

    def transform(self, type: CharacterType):
        if self.type == type:
            return self

        new_character: BaseCharacter = CharacterTypes.get(type)
        
        if new_character is not None:
            new_character = new_character(self.space, helpers.transform_to_pymunk(self.x, self.y, self.width, self.height), (self.original_width, self.original_height))

            new_character.body.velocity = self.body.velocity
            new_character.body.angular_velocity = self.body.angular_velocity
            
            new_character.show_hitbox = self.show_hitbox

            self.space.remove(self.body, self.shape)

            new_character.post_transform()

        return new_character

    def handle_movement(self, keys):
        pass

    def velocity_adjustments(self):
        pass

    def update_location(self):
        pass

    def _get_image(self):
        return self.image

    def kill(self, level):
        pass

    def update_location(self):
        self.x, self.y = helpers.transform_to_pygame(*self.body.position, self.width, self.height)

    def draw(self, win):
        win.blit(self._get_image(), (self.x, self.y))

        if self.show_hitbox:
            pygame.draw.rect(win, Colors.RED, self.rect, 2)

    


class Blob(BaseCharacter):
    def __init__(self, space, pos: tuple, size: tuple):
        super().__init__(space, pos, size)

        self.type = CharacterType.BLOB

        self.image = Fonts.CHARACTER.render("BLOB", True, Colors.WHITE)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def setup_physics(self):
        try:
            self.space.remove(self.body, self.shape)
        except AttributeError:
            pass

        self.body = pymunk.Body()
        self.body.position = self.x, self.y
        self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
        self.shape.mass = 1
        self.shape.friction = 0.99
        self.shape.elasticity = 0.2
        self.shape.collision_type = CollisionType.CHARACTER

        self.space.add(self.body, self.shape)

        self.MAX_X_VELOCITY = 300

    def handle_movement(self, keys):
        floored = self.is_floored()
        if not floored:
            self.body.velocity = (self.body.velocity.x * 0.99, self.body.velocity.y)

        if keys[pygame.K_LEFT]:
            if not self.body.velocity.x < -self.MAX_X_VELOCITY:
                self.body.apply_impulse_at_local_point((-50, 0))
        if keys[pygame.K_RIGHT]:
            if not self.body.velocity.x > self.MAX_X_VELOCITY:
                self.body.apply_impulse_at_local_point((50, 0))
        if keys[pygame.K_UP]:
            if floored:
                self.body.apply_impulse_at_local_point((0, -500))


    def is_floored(self):
        for terrain in Level.get_current_level().terrain:
            if not self.rect.colliderect(terrain.rect.copy().inflate(2, 2)):
                continue

            if not terrain.x < self.rect.centerx < terrain.x + terrain.width:
                continue

            if not terrain.y > self.rect.centery:
                continue

            break
        else:
            return False

        return True

    def velocity_adjustments(self):
        self.body.angular_velocity = 0

    def update_location(self):
        self.x, self.y = helpers.transform_to_pygame(*self.body.position, self.width, self.height)

    


class Airplane(BaseCharacter):
    def __init__(self, space, pos: tuple, size: tuple):
        super().__init__(space, pos, size)

        self.width = self.original_width // 2
        self.height = self.original_height // 2

        self.type = CharacterType.AIRPLANE

        # self.image = Fonts.CHARACTER.render("PLANE", True, Colors.WHITE)
        self.image = pygame.transform.scale(self.image, (self.original_width, self.height))

        self.setup_physics()

    def setup_physics(self):
        try:
            self.space.remove(self.body, self.shape)
        except AttributeError:
            pass

        self.body = pymunk.Body()
        self.body.position = self.x, self.y
        self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
        self.shape.mass = 0.25
        self.shape.friction = 0.99
        self.shape.elasticity = 0
        self.shape.collision_type = CollisionType.CHARACTER

        self.agility = 5

        self.body.velocity_func = lambda body, gravity, damping, dt: pymunk.Body.update_velocity(body, (gravity[0], gravity[1] * 0.7), damping, dt)

        self.space.add(self.body, self.shape)

    def post_transform(self):
        try:
            self.direction = self.body.velocity.x / abs(self.body.velocity.x)
        except ZeroDivisionError:
            self.direction = 1

    def handle_movement(self, keys):
        velocity_magnitude = math.sqrt(self.body.velocity.x ** 2 + self.body.velocity.y ** 2)
        angle = math.atan2(self.body.velocity.y, self.body.velocity.x)

        if keys[pygame.K_UP]:
            angle -= 0.01 * self.direction * self.agility
        if keys[pygame.K_DOWN]:
            angle += 0.01 * self.direction * self.agility

        self.body.velocity = (velocity_magnitude * math.cos(angle), velocity_magnitude * math.sin(angle))


    def _get_image(self):
        angle = math.degrees(math.atan2(self.body.velocity.y, self.body.velocity.x))
        if self.direction == 1:
            image = self.image
            image = pygame.transform.rotate(image, -angle)

        else:
            image = pygame.transform.flip(self.image, True, False)
            image = pygame.transform.rotate(image, -angle - 180)

        return image

    def draw(self, win):
        win.blit(self._get_image(), (self.x - self.original_width // 4, self.y))

        if self.show_hitbox:
            pygame.draw.rect(win, Colors.RED, self.rect, 2)

        






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

CharacterTypes = {
    CharacterType.BLOB: Blob,
    CharacterType.AIRPLANE: Airplane,
    CharacterType.SPRING: Spring,
    CharacterType.WEIGHT: Weight,
    CharacterType.PLUNGER: Plunger
}