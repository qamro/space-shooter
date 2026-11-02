import pygame
import random
import math

pygame.init()


# set the game configuration
WIDTH, HEIGHT = 420, 640
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Space Shooter")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("consolas", 24, bold=True)
SMALL = pygame.font.SysFont("consolas", 16)

BG = (7, 5, 20)
WHITE = (245, 245, 255)
PURPLE = (185, 70, 255)
CYAN = (80, 220, 255)
RED = (255, 70, 110)
PINK = (255, 90, 210)
YELLOW = (255, 220, 90)