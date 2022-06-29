from level import Level
from terrain import *
from constants import *

"""
Did some testing and it seems that the max jump height is about 150 pixels.

Remember that the top left is (0, 0) and the bottom right is (WIDTH, HEIGHT).

Need to determine the max jump distance.

To change the current level, you can change a line of code in the setup() function in main.py.
"""

level_1 = Level("level1", 1, (350, 350))

# Borders
level_1.add_terrain(Floor(0, Screen.HEIGHT - 50, Screen.WIDTH, 50))
level_1.add_terrain(Floor(Screen.WIDTH - 50, 0, 50, Screen.HEIGHT))
level_1.add_terrain(Floor(0, 0, Screen.WIDTH, 50))
level_1.add_terrain(Floor(0, 0, 50, Screen.HEIGHT))

# Platforms
level_1.add_terrain(Floor(300, 450, 150, 20))
level_1.add_terrain(Floor(650, 400, 150, 50))
level_1.add_terrain(Floor(850, 250, 150, 30))
level_1.add_terrain(Floor(450, 200, 100, 20))

# Lava
level_1.add_terrain(Lava(50, Screen.HEIGHT -
                    50, Screen.WIDTH - 100, 25))

# Trampoline
level_1.add_terrain(Trampoline(Screen.WIDTH - 60, 100, 25, 120, 40))


level_2 = Level("level2", 2, (350, 350))

# Trampoline borders
level_2.add_terrain(Trampoline(0, Screen.HEIGHT - 50, Screen.WIDTH, 50, 25))
level_2.add_terrain(Trampoline(Screen.WIDTH - 50, 0, 50, Screen.HEIGHT, 55))
level_2.add_terrain(Trampoline(0, 0, Screen.WIDTH, 50, 25))
level_2.add_terrain(Trampoline(0, 0, 50, Screen.HEIGHT, 55))
