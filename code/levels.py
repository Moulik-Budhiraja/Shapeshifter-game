from level import Level
from terrain import *
from constants import *

"""
Did some testing and it seems that the max jump height is about 150 pixels.

Remember that the top left is (0, 0) and the bottom right is (WIDTH, HEIGHT).

Need to determine the max jump distance.

To change the current level, you can change a line of code in the setup() function in main.py.
"""


def generate_levels():
    level_1 = Level("level1", 1, (100, Screen.HEIGHT - 100))

    # Borders
    level_1.add_terrain(Floor(0, Screen.HEIGHT - 25, Screen.WIDTH, 25))
    level_1.add_terrain(Wall(0, 0, Screen.WIDTH, 25))
    level_1.add_terrain(Wall(0, 0, 25, Screen.HEIGHT))
    level_1.add_terrain(Wall(Screen.WIDTH - 25, 0, 25, Screen.HEIGHT))

    # Ramp
    level_1.add_terrain(Polygon((500, Screen.HEIGHT - 25), (530, Screen.HEIGHT - 25), (700, 550), (630, 550), (500, Screen.HEIGHT - 25)))

    # Goal
    level_1.add_terrain(Goal(Screen.WIDTH - 100, Screen.HEIGHT - 100, 50, 50))

    level_2 = Level("level2", 2, (100, Screen.HEIGHT - 300))

    # Borders
    level_2.add_terrain(Floor(0, Screen.HEIGHT - 25, Screen.WIDTH, 25))
    level_2.add_terrain(Floor(Screen.WIDTH - 25, 0, 25, Screen.HEIGHT))
    level_2.add_terrain(Floor(0, 0, Screen.WIDTH, 25))
    level_2.add_terrain(Floor(0, 0, 25, Screen.HEIGHT))

    # Platforms
    level_2.add_terrain(Floor(0, Screen.HEIGHT - 225, 200, 225))
    level_2.add_terrain(Floor(Screen.WIDTH - 200, Screen.HEIGHT - 325, 200, 325))
    level_2.add_terrain(Floor(275, 350, 125, 20))
    level_2.add_terrain(Floor(475, 275, 125, 20))
    level_2.add_terrain(Floor(700, 275, 125, 20))

    # Lava
    level_2.add_terrain(Lava(200, Screen.HEIGHT - 50, Screen.WIDTH - 400, 25))

    # Goal
    level_2.add_terrain(Goal(Screen.WIDTH - 100, Screen.HEIGHT - 400, 50, 50))

    level_3 = Level("level3", 3, (100, Screen.HEIGHT - 450))

    # Borders
    level_3.add_terrain(Floor(0, Screen.HEIGHT - 25, Screen.WIDTH, 25))
    level_3.add_terrain(Floor(Screen.WIDTH - 25, 0, 25, Screen.HEIGHT))
    level_3.add_terrain(Floor(0, 0, Screen.WIDTH, 25))
    level_3.add_terrain(Floor(0, 0, 25, Screen.HEIGHT))

    # Lava
    level_3.add_terrain(Lava(225, Screen.HEIGHT - 50, Screen.WIDTH - 425, 25))

    # Platforms
    level_3.add_terrain(Floor(25, Screen.HEIGHT - 400, 200, 375))
    level_3.add_terrain(Floor(Screen.WIDTH - 200, Screen.HEIGHT - 75, 175, 50))
    level_3.add_terrain(Floor(700, 25, 50, 325))
    level_3.add_terrain(Floor(700, 500, 50, 180))

    # Goal
    level_3.add_terrain(Goal(Screen.WIDTH - 100, Screen.HEIGHT - 150, 50, 50))

    level_4 = Level("level4", 4, (100, Screen.HEIGHT - 500))

    # Goal
    level_4.add_terrain(Goal(0, Screen.HEIGHT - 100, Screen.WIDTH, 100, target=1))
