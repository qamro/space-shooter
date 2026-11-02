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


# stars
stars = []
for _ in range(90):
    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.choice([1, 1, 1, 2]),
        random.uniform(0.4, 1.5)
    ])

def update_stars():
    for s in stars:
        s[1] += s[3]
        if s[1] > HEIGHT:
            s[0] = random.randint(0, WIDTH)
            s[1] = 0

def draw_stars():
    for x, y, r, _ in stars:
        pygame.draw.circle(screen, (150, 140, 210), (int(x), int(y)), r)


# particles 
particles = []

def spawn_explosion(x, y, color, amount=22):
    for _ in range(amount):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(1.5, 5.5)
        particles.append({
            "x": x,
            "y": y,
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "life": random.randint(18, 36),
            "size": random.randint(2, 5),
            "color": color,
        })

def update_particles():
    for p in particles[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vx"] *= 0.97
        p["vy"] *= 0.97
        p["life"] -= 1
        p["size"] = max(1, p["size"] - 0.05)
        if p["life"] <= 0:
            particles.remove(p)

def draw_particles():
    for p in particles:
        surf = pygame.Surface((18, 18), pygame.SRCALPHA)
        alpha = max(0, min(255, p["life"] * 8))
        pygame.draw.circle(
            surf,
            (*p["color"], alpha),
            (9, 9),
            int(p["size"])
        )
        screen.blit(surf, (p["x"] - 9, p["y"] - 9))