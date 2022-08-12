import pygame
import os

class Characters:
    try:
        class Blob:
            JUMPING = [pygame.image.load(os.path.join('..', 'assets', 'images', 'characters', 'blob', 'Jumping', f'SG Jump {i}.png')) for i in range(1, 8)]
            WALKING = [pygame.image.load(os.path.join('..', 'assets', 'images', 'characters', 'blob', 'Walking', f'SG Walk {i}.png')) for i in range(1, 4)]
            IDLE = pygame.image.load(os.path.join('..', 'assets', 'images', 'characters', 'blob', 'SG Idle.png'))
        
        class Plane:
            PLANE = pygame.image.load(os.path.join('..', 'assets', 'images', 'characters', 'plane', 'SG Plane Up.png'))
            TRANSFORM = [pygame.image.load(os.path.join('..', 'assets', 'images', 'characters', 'plane', f'SG Plane Transform {i}.png')) for i in range(1, 3)]

        class Weight:
            BALL = pygame.image.load(os.path.join('..', 'assets', 'images', 'characters', 'metal ball', 'SG Ball.png'))
            TRANSFORM = [pygame.image.load(os.path.join('..', 'assets', 'images', 'characters', 'metal ball', f'SG Ball Transform {i}.png')) for i in range(1, 3)]

    
    except FileNotFoundError:
        class Blob:
            JUMPING = [pygame.image.load(os.path.join('assets', 'images', 'characters', 'blob', 'Jumping', f'SG Jump {i}.png')) for i in range(1, 8)]
            WALKING = [pygame.image.load(os.path.join('assets', 'images', 'characters', 'blob', 'Walking', f'SG Walk {i}.png')) for i in range(1, 4)]
            IDLE = pygame.image.load(os.path.join('assets', 'images', 'characters', 'blob', 'SG Idle.png'))
        
        class Plane:
            PLANE = pygame.image.load(os.path.join('assets', 'images', 'characters', 'plane', 'SG Plane Up.png'))
            TRANSFORM = [pygame.image.load(os.path.join('assets', 'images', 'characters', 'plane', f'SG Plane Transform {i}.png')) for i in range(1, 3)]

        class Weight:
            BALL = pygame.image.load(os.path.join('assets', 'images', 'characters', 'metal ball', 'SG Ball.png'))
            TRANSFORM = [pygame.image.load(os.path.join('assets', 'images', 'characters', 'metal ball', f'SG Ball Transform {i}.png')) for i in range(1, 3)]