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
        


# the player
class Player:
    def __init__(self):
        self.w = 38
        self.h = 50
        self.x = WIDTH // 2
        self.y = HEIGHT - 80
        self.speed = 6
        self.cooldown = 0
        self.alive = True

    @property
    def rect(self):
        return pygame.Rect(
            self.x - self.w // 2,
            self.y - self.h // 2,
            self.w,
            self.h
        )

    def update(self, keys):
        if not self.alive:
            return

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

        self.x = max(self.w // 2, min(WIDTH - self.w // 2, self.x))
        self.y = max(80, min(HEIGHT - self.h // 2 - 8, self.y))

        if self.cooldown > 0:
            self.cooldown -= 1

    def shoot(self):
        if self.alive and self.cooldown <= 0:
            bullets.append(Bullet(self.x - 7, self.y - 28))
            bullets.append(Bullet(self.x + 7, self.y - 28))
            self.cooldown = 10

    def draw(self):
        x, y = int(self.x), int(self.y)

        # engine glow
        glow = pygame.Surface((80, 90), pygame.SRCALPHA)
        pygame.draw.circle(glow, (110, 60, 255, 40), (40, 45), 34)
        screen.blit(glow, (x - 40, y - 38))

        # ship body
        pygame.draw.polygon(
            screen,
            WHITE,
            [(x, y - 26), (x - 17, y + 18), (x, y + 10), (x + 17, y + 18)],
            2
        )
        pygame.draw.polygon(
            screen,
            PURPLE,
            [(x, y - 22), (x - 8, y + 12), (x, y + 7), (x + 8, y + 12)],
            2
        )

        # wings
        pygame.draw.line(screen, WHITE, (x - 17, y + 17), (x - 25, y + 25), 2)
        pygame.draw.line(screen, WHITE, (x + 17, y + 17), (x + 25, y + 25), 2)

        # flame
        if self.alive:
            flame_h = random.randint(8, 18)
            pygame.draw.polygon(
                screen,
                CYAN,
                [(x - 4, y + 17), (x, y + 17 + flame_h), (x + 4, y + 17)]
            )
