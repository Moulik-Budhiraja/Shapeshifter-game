import pygame
import pymunk
from constants import *
from characters import *
import helpers
import math


class Terrain:
    def __init__(self, x, y, width, height, jumpable: bool = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.starting_x = x
        self.starting_y = y

        self.jumpable = jumpable

        self.level: Level = None

    def __repr__(self) -> str:
        return f"Terrain({self.x}, {self.y}, {self.width}, {self.height})"

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    @property
    def polygon(self):
        return [self.rect.topleft, self.rect.topright, self.rect.bottomright, self.rect.bottomleft]

    def setup_physics(self, collision_type: int):
        try:
            self.level.space.remove(self.body, self.shape)
        except AttributeError:
            pass
        except AssertionError:
            pass

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = helpers.transform_to_pymunk(self.x, self.y, self.width, self.height)

        self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
        self.shape.friction = 0.5
        self.shape.elasticity = 0.5

        self.level.space.add(self.body, self.shape)

        self.shape.collision_type = collision_type

        try:
            del self.collision_handler
        except AttributeError:
            pass
        finally:
            self.collision_handler = self.level.space.add_collision_handler(collision_type, CollisionType.CHARACTER)

        self.collision_handler.begin = self.collision_callback

    def collision_callback(self, arbiter, space, data):
        return True
    
    def reset(self, collision_type: int):
        self.x = self.starting_x
        self.y = self.starting_y

        self.setup_physics(collision_type)

    def draw(self, win):
        pygame.draw.rect(win, Colors.DARK_GRAY3, self.rect)

        if self.level.character.show_hitbox:
            pygame.draw.rect(win, Colors.RED, self.rect, 2)


class Floor(Terrain):
    def __init__(self, x, y, width, height, jumpable: bool = True):
        super().__init__(x, y, width, height, jumpable)

    def __repr__(self) -> str:
        return f"Floor({self.x}, {self.y}, {self.width}, {self.height})"

    def setup_physics(self, collision_type: int):
        super().setup_physics(collision_type)

    def draw(self, win):
        pygame.draw.rect(win, Colors.DARK_GRAY, self.rect)

        if self.level.character.show_hitbox:
            pygame.draw.rect(win, Colors.RED, self.rect, 2)


class Wall(Terrain):
    def __init__(self, x, y, width, height, jumpable: bool = False):
        super().__init__(x, y, width, height, jumpable)

    def __repr__(self) -> str:
        return f"Wall({self.x}, {self.y}, {self.width}, {self.height})"

    def setup_physics(self, collision_type: int):
        super().setup_physics(collision_type)

        self.shape.friction = 0

    def draw(self, win):
        pygame.draw.rect(win, Colors.DARK_GRAY, self.rect)

        if self.level.character.show_hitbox:
            pygame.draw.rect(win, Colors.RED, self.rect, 2)


class Polygon(Terrain):
    def __init__(self, *vertices, jumpable: bool = True):
        x_points = [vertex[0] for vertex in vertices]
        y_points = [vertex[1] for vertex in vertices]

        self.x = min(x_points)
        self.y = min(y_points)
        self.width = max(x_points) - self.x
        self.height = max(y_points) - self.y

        super().__init__(self.x, self.y, self.width, self.height, jumpable)

        self.vertices = vertices

    def __repr__(self) -> str:
        return f"Polygon({self.vertices})"

    @property
    def polygon(self):
        return self.vertices

    def setup_physics(self, collision_type: int):
        try:
            self.level.space.remove(self.body, self.shape)
        except AttributeError:
            pass
        except AssertionError:
            pass

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (0, 0)

        self.shape = pymunk.Poly(self.body, self.vertices)
        self.shape.friction = 0.5
        self.shape.elasticity = 0.5

        self.level.space.add(self.body, self.shape)

        self.shape.collision_type = collision_type

        try:
            del self.collision_handler
        except AttributeError:
            pass
        finally:
            self.collision_handler = self.level.space.add_collision_handler(collision_type, CollisionType.CHARACTER)

    def draw(self, win):
        # pygame.draw.rect(win, Colors.DARK_GRAY, self.rect)

        pygame.draw.polygon(win, Colors.DARK_GRAY, [v for v in self.shape.get_vertices()])


        if self.level.character.show_hitbox:
            pygame.draw.polygon(win, Colors.RED, [v for v in self.shape.get_vertices()], 2)

            for vertex in self.shape.get_vertices():
                pygame.draw.circle(win, Colors.RED, vertex, 3)




class Lava(Terrain):
    def __init__(self,  x, y, width, height, jumpable: bool = False):
        super().__init__( x, y, width, height, jumpable)

    def __repr__(self) -> str:
        return f"Lava({self.x}, {self.y}, {self.width}, {self.height})"

    
    def setup_physics(self, collision_type: int):
        super().setup_physics(collision_type)

        self.collision_handler.begin = self.collision_callback

    def collision_callback(self, arbiter, space, data):
        character = self.level.character

        character.set_level(Level.get_level(Level.current_level))

        return False

    def draw(self, win):
        pygame.draw.rect(win, Colors.RED, self.rect)

        if self.level.character.show_hitbox:
            pygame.draw.rect(win, Colors.RED, self.rect, 2)


class Trampoline(Terrain):
    def __init__(self,  x, y, width, height, power, jumpable: bool = True):
        super().__init__( x, y, width, height, jumpable)

        self.power = power

    def __repr__(self) -> str:
        return f"Trampoline({self.x}, {self.y}, {self.width}, {self.height})"

    def setup_physics(self, collision_type: int):
        super().setup_physics(collision_type)

        self.shape.elasticity *= self.power

    def draw(self, win):
        pygame.draw.rect(win, Colors.BLUE, self.rect)

        if self.level.character.show_hitbox:
            pygame.draw.rect(win, Colors.RED, self.rect, 2)


class Goal(Terrain):
    def __init__(self,  x, y, width, height, target=None, jumpable: bool = False):
        super().__init__( x, y, width, height, jumpable)

        self.target = target

    def __repr__(self) -> str:
        return f"Goal({self.x}, {self.y}, {self.width}, {self.height})"

    def setup_physics(self, collision_type: int):
        super().setup_physics(collision_type)

        self.collision_handler.begin = self.collision_callback

    def collision_callback(self, arbiter, space, data):
        character = self.level.character

        if self.target != None:
            character.set_level(Level.get_level(self.target))
        else:
            character.set_level(Level.get_level(Level.current_level + 1))

        return False

    def draw(self, win):
        pygame.draw.rect(win, Colors.GREEN, self.rect)

        if self.level.character.show_hitbox:
            pygame.draw.rect(win, Colors.RED, self.rect, 2)


