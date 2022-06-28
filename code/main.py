import pygame
pygame.init()

multiplyer = 70

WIDTH = 16 * multiplyer
HEIGHT = 9 * multiplyer

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

print(WIDTH, HEIGHT)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()
