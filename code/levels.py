from level import Level
from terrain import *
from constants import *

"""
Did some testing and it seems that the max jump height is about 150 pixels.

Remember that the top left is (0, 0) and the bottom right is (WIDTH, HEIGHT).

Need to determine the max jump distance.

To change the current level, you can change a line of code in the setup() function in main.py.
"""

def platform(level, x, y, width, height, thickness=2):
    level.add_terrain(Floor(x, y, width, thickness))
    level.add_terrain(Wall(x, y + thickness, width, height - thickness))


def generate_levels():
    level_1 = Level("level1", 1, (100, Screen.HEIGHT - 100))

    # Borders
    level_1.add_terrain(Floor(0, Screen.HEIGHT - 25, Screen.WIDTH, 25))
    level_1.add_terrain(Wall(0, 0, Screen.WIDTH, 25))
    level_1.add_terrain(Wall(0, 0, 25, Screen.HEIGHT))
    level_1.add_terrain(Wall(Screen.WIDTH - 25, 0, 25, Screen.HEIGHT))

    # Ramp
    level_1.add_terrain(Polygon((25, Screen.HEIGHT - 75), (75, Screen.HEIGHT - 25), (25, Screen.HEIGHT - 25)))

    # Goal
    level_1.add_terrain(Goal(Screen.WIDTH - 100, Screen.HEIGHT - 100, 50, 50))

    level_2 = Level("level2", 2, (100, Screen.HEIGHT - 300))

    # Borders
    level_2.add_terrain(Floor(0, Screen.HEIGHT - 25, Screen.WIDTH, 25))
    level_2.add_terrain(Wall(Screen.WIDTH - 25, 0, 25, Screen.HEIGHT))
    level_2.add_terrain(Wall(0, 0, Screen.WIDTH, 25))
    level_2.add_terrain(Wall(0, 0, 25, Screen.HEIGHT))

    # Platforms
    platform(level_2, 0, Screen.HEIGHT - 225, 200, 225)
    platform(level_2, Screen.WIDTH - 200, Screen.HEIGHT - 325, 200, 325)
    platform(level_2, 275, 350, 125, 20)
    platform(level_2, 475, 275, 125, 20)
    platform(level_2, 700, 275, 125, 20)

    # Lava
    level_2.add_terrain(Lava(200, Screen.HEIGHT - 50, Screen.WIDTH - 400, 25))

    # Goal
    level_2.add_terrain(Goal(Screen.WIDTH - 100, Screen.HEIGHT - 400, 50, 50))

    level_3 = Level("level3", 3, (100, Screen.HEIGHT - 450))

    # Borders
    level_3.add_terrain(Floor(0, Screen.HEIGHT - 25, Screen.WIDTH, 25))
    level_3.add_terrain(Wall(Screen.WIDTH - 25, 0, 25, Screen.HEIGHT))
    level_3.add_terrain(Wall(0, 0, Screen.WIDTH, 25))
    level_3.add_terrain(Wall(0, 0, 25, Screen.HEIGHT))

    # Lava
    level_3.add_terrain(Lava(225, Screen.HEIGHT - 50, Screen.WIDTH - 425, 25))

    # Platforms
    platform(level_3, 25, Screen.HEIGHT - 400, 200, 375)
    platform(level_3, Screen.WIDTH - 200, Screen.HEIGHT - 75, 175, 50)
    platform(level_3, 700, 25, 50, 325)
    platform(level_3, 700, 500, 50, 180)

    # Goal
    level_3.add_terrain(Goal(Screen.WIDTH - 100, Screen.HEIGHT - 150, 50, 50))

    level_4 = Level("level4", 4, (100, Screen.HEIGHT - 85))

    #Level 4 Borders
    level_4.add_terrain(Floor(0, Screen.HEIGHT - 25, Screen.WIDTH, 25))
    level_4.add_terrain(Wall(Screen.WIDTH - 25, 0, 25, Screen.HEIGHT))
    level_4.add_terrain(Wall(0, 0, Screen.WIDTH, 25))
    level_4.add_terrain(Wall(0, 0, 25, Screen.HEIGHT))

    #Level 4 Tramampoline
    level_4.add_terrain(Trampoline(400, Screen.HEIGHT - 25, 50, 15, 12))

    #First slide under
    platform(level_4, 250, 0, 50, Screen.HEIGHT - 60)
    #Big ass box
    platform(level_4, 490, 100, 200, Screen.HEIGHT)
    #Top ball go under
    platform(level_4, 580, 25, 25, 24)
    #Lava
    level_4.add_terrain(Lava(690, 150, 35, 25))
    #Piece underneath lava
    platform(level_4, 690, 175, 35, Screen.HEIGHT)
    #Extra Catching piece
    platform(level_4, 725, 100, 75, Screen.HEIGHT)
    #Drop piece leading to goal (EXTRA BIG ASS BOX)
    platform(level_4, 830, 25, Screen.WIDTH, 515)
    # Goal
    level_4.add_terrain(Goal(Screen.WIDTH - 50 , 540, 25, 65))

    level_5 = Level("level5", 5, (100, Screen.HEIGHT - 500))
    
    #Level 5 borders
    level_5.add_terrain(Floor(0, Screen.HEIGHT - 25, Screen.WIDTH, 25))
    level_5.add_terrain(Wall(Screen.WIDTH - 25, 0, 25, Screen.HEIGHT))
    level_5.add_terrain(Wall(0, 0, Screen.WIDTH, 25))
    level_5.add_terrain(Wall(0, 0, 25, Screen.HEIGHT))

    #Level 5 Big box
    platform(level_5, 25, 150, 195, Screen.HEIGHT)
    #Level 5 Ramp

    level_5.add_terrain(Polygon((220, 150), (285, 315), (375, 400), (420, 425), (460, 450), (510, 460), (600, 450), (620, 445), (650, 430), (675, 400), (675, 605), (220, 605)))



    # # Level 5 Tramampoline
    # level_5.add_terrain(Trampoline(250, Screen.HEIGHT - 25, 75, 25, 50))
    # # Level 5 Polygon triangle thingy
    # level_5.add_terrain(Polygon((250, 300), (500, 25), (250, 25), jumpable=False))
    # #Level 5 second bounce triangle
    # level_5.add_terrain(Polygon((750, 25), (500, 25), (750, 300), jumpable=False))
    # #Level 5 Triangle on big ass box
    # level_5.add_terrain(Polygon((330, 350), (495, 260), (660, 350), jumpable=False))
    # #Level 5 big ass box
    # platform(level_5, 330, 350, 330, 330)
    # #Level 
    