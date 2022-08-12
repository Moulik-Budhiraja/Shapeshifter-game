import pygame
import pymunk
from level import Level
from constants import *
from animations import Animation
import helpers
import math
import images
import matplotlib.path as mplpath

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

        self.show_hitbox = True

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def setup_physics(self):
        pass

    def post_transform(self):
        pass

    def set_level(self, level: Level):
        Level.current_level = level.number
        level.reset()

        pygame.event.post(pygame.event.Event(Events.CHARACTER_DIE))

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

        self.image = images.Characters.Blob.IDLE
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def setup_physics(self):
        try:
            self.space.remove(self.body, self.shape)
        except AttributeError:
            pass
        except AssertionError:
            pass

        self.body = pymunk.Body()
        self.body.position = self.x, self.y
        self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
        self.shape.mass = 1
        self.shape.friction = 0.90
        self.shape.elasticity = 0
        self.shape.collision_type = CollisionType.CHARACTER

        self.jump_strength = 1.3
        self.gravity = 3.5

        self.body.velocity_func = lambda body, gravity, damping, dt: pymunk.Body.update_velocity(body, (gravity[0], gravity[1] * self.gravity), damping, dt)

        self.space.add(self.body, self.shape)

        self.MAX_X_VELOCITY = 300

    def handle_movement(self, keys):
        in_air = self._in_air()
        if in_air:
            self.body.velocity = (self.body.velocity.x * 0.99, self.body.velocity.y)
            self.body.angle = 0
            self.body.angular_velocity = 0

        if keys[pygame.K_LEFT]:
            if not self.body.velocity.x < -self.MAX_X_VELOCITY:
                self.body.apply_impulse_at_local_point((-50, 0), (0, 15))
        if keys[pygame.K_RIGHT]:
            if not self.body.velocity.x > self.MAX_X_VELOCITY:
                self.body.apply_impulse_at_local_point((50, 0), (0, 15))
        if keys[pygame.K_UP]:
            if not in_air:
                self.body.apply_impulse_at_local_point((0, -750 * self.jump_strength))


        

    def _in_air(self):
        bottom = self.shape.bb.top
        right = self.shape.bb.right
        left = self.shape.bb.left

        if self.body.angle < 0:
            point1 = (right, bottom + self.width * math.sin(self.body.angle) + 1)
            point2 = (right - self.width * math.cos(self.body.angle), bottom + 1)

        else:
            point1 = (left, bottom - self.width * math.sin(self.body.angle) + 1)
            point2 = (left + self.width * math.cos(self.body.angle), bottom + 1)

        
        for terrain in Level.get_current_level().terrain:
            path = mplpath.Path(terrain.polygon)
            if path.contains_point(point1) or path.contains_point(point2):
                return False

        return True


    def velocity_adjustments(self):
        if self.body.angle > 0.523599: # 30 degrees
            self.body.angular_velocity = -1.5
        elif self.body.angle < -0.523599: 
            self.body.angular_velocity = 1.5

    def update_location(self):
        self.x, self.y = helpers.transform_to_pygame(*self.body.position, self.width, self.height)

    def _get_image(self):
        return pygame.transform.rotate(self.image, math.degrees(-self.body.angle))

    def draw(self, win):
        image = self._get_image()
        rect = image.get_rect()
        rect.center = helpers.transform_to_pymunk(self.x, self.y + 2, self.width, self.height)

        # win.blit(image, rect)

        if self.show_hitbox:
            temp_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA, 32)
            temp_surface = temp_surface.convert_alpha()
            pygame.draw.rect(temp_surface, Colors.RED, (0, 0, self.rect.width, self.rect.height), 2)

            win.blit(pygame.transform.rotate(temp_surface, math.degrees(-self.body.angle)), rect)

            pygame.draw.circle(win, Colors.RED, self.body._get_position(), 2)

            # pygame.draw.circle(win, Colors.BLACK, self.rect.bottomright, 2)

            # pygame.draw.circle(win, Colors.RED, (self.shape.bb.left, self.shape.bb.bottom), 2)
            # pygame.draw.circle(win, Colors.RED, (self.shape.bb.right, self.shape.bb.bottom), 2)

            bottom = self.shape.bb.top
            right = self.shape.bb.right
            left = self.shape.bb.left

            if self.body.angle < 0:
                point1 = (right, bottom + self.width * math.sin(self.body.angle) + 1)
                point2 = (right - self.width * math.cos(self.body.angle), bottom + 1)

            else:
                point1 = (left, bottom - self.width * math.sin(self.body.angle) + 1)
                point2 = (left + self.width * math.cos(self.body.angle), bottom + 1)

            pygame.draw.circle(win, Colors.GREEN, point1, 2)
            pygame.draw.circle(win, Colors.GREEN, point2, 2)


    


class Airplane(BaseCharacter):
    def __init__(self, space, pos: tuple, size: tuple):
        super().__init__(space, pos, size)

        self.width = self.original_width // 2
        self.height = self.original_height // 2

        self.type = CharacterType.AIRPLANE

        # self.image = images.Characters.Plane.PLANE
        self.image = pygame.transform.scale(self.image, (self.original_width, self.height))

        self.setup_physics()

    def setup_physics(self):
        try:
            self.space.remove(self.body, self.shape)
        except AttributeError:
            pass
        except AssertionError:
            pass

        self.body = pymunk.Body()
        self.body.position = self.x, self.y
        self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
        self.shape.mass = 0.25
        self.shape.friction = 0.99
        self.shape.elasticity = 0
        self.shape.collision_type = CollisionType.CHARACTER

        self.agility = 5
        self.gravity = 0.7

        self.body.velocity_func = lambda body, gravity, damping, dt: pymunk.Body.update_velocity(body, (gravity[0], gravity[1] * self.gravity), damping, dt)

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

        self.body.velocity = (velocity_magnitude * math.cos(angle) * 0.99, velocity_magnitude * math.sin(angle))


    def _get_image(self):
        angle = math.degrees(math.atan2(self.body.velocity.y, self.body.velocity.x))
        if abs(self.body.velocity.x) < 0.01 and abs(self.body.velocity.y) < 0.01:
            if self.direction == 1:
                angle = 0
            else:
                angle = -180

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

    def velocity_adjustments(self):
        self.body.angular_velocity = 0



class Spring(BaseCharacter):
    def __init__(self, space, pos: tuple, size: tuple):
        super().__init__(space, pos, size)

        self.type = CharacterType.SPRING

        self.image = Fonts.CHARACTER.render("SPRING", True, Colors.WHITE)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


class Weight(BaseCharacter):
    def __init__(self, space, pos: tuple, size: tuple):
        super().__init__(space, pos, size)

        self.width = self.original_width // 2
        self.height = self.original_height // 2

        self.image = images.Characters.Weight.BALL
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.type = CharacterType.WEIGHT

        self.setup_physics()

    def setup_physics(self):
        try:
            self.space.remove(self.body, self.shape)
        except AttributeError:
            pass
        except AssertionError:
            pass

        self.body = pymunk.Body()
        self.body.position = self.x, self.y
        self.shape = pymunk.Circle(self.body, self.width // 2)
        self.shape.mass = 1
        self.shape.friction = 0
        self.shape.elasticity = 0
        self.shape.collision_type = CollisionType.CHARACTER

        self.gravity = 8

        self.body.velocity_func = lambda body, gravity, damping, dt: pymunk.Body.update_velocity(body, (gravity[0], gravity[1] * self.gravity), damping, dt)

        self.space.add(self.body, self.shape)

    def draw(self, win):
        # win.blit(self._get_image(), (self.x, self.y))

        if self.show_hitbox:
            pygame.draw.circle(win, Colors.RED, helpers.transform_to_pymunk(self.x, self.y, self.width, self.height), self.width // 2, 2)


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