import os
import sys
import random
import pygame
import pygame_gui


FPS = 60
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 960


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


pygame.init()
pygame.display.set_caption('ROAD RAGE')
screen = pygame.display.set_mode(WINDOW_SIZE)

background = pygame.Surface(WINDOW_SIZE)
background.fill((0, 0, 0))

char = [load_image('player1.png'), load_image(
    'player2.png'), load_image('player3.png')]

clock = pygame.time.Clock()


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7
        self.rideCount = 0

    def draw(self, screen):
        if self.rideCount + 1 >= 15:
            self.rideCount = 0
        screen.blit(char[self.rideCount // 5], (self.x, self.y))
        self.rideCount += 1


class Enemy(object):
    en = [load_image('enemy1_1.png'), load_image(
        'enemy1_2.png'), load_image('enemy1_3.png')]

    def __init__(self, x, y, width, height, speed, end, velocity):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.y, self.end]
        self.rideCount = 0
        self.speed = speed
        self.velocity = velocity

    def draw(self, screen):
        self.move()
        self.shoot()
        if self.rideCount + 1 >= 9:
            self.rideCount = 0
        screen.blit(self.en[self.rideCount // 3], (self.x, self.y))
        self.rideCount += 1

    def move(self):
        if self.y + self.speed < self.path[1]:
            self.y += self.speed
        else:
            self.speed = 0

    def shoot(self):
        if self.speed == 0:
            if random.randrange(0, self.velocity * FPS) == 1:
                bullets.append(Projectile(
                    round(self.x + self.width // 2), round(self.y + self.height), 3, (255, 255, 225), 14, 1))


class Projectile(object):
    def __init__(self, x, y, radius, color, speed, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.speed = speed * facing

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


def redrawGameWindow():
    screen.blit(background, (0, 0))
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.update()


player = Player(100, 100, 30, 30)
bullets = []
enemies = [Enemy(random.randrange(0, WINDOW_WIDTH - 50), 0, 50,
                 50, 4, random.randrange(50, WINDOW_HEIGHT - 500), 3) for _ in range(random.randrange(3, 11))]
prev_time = pygame.time.get_ticks()


running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for bullet in bullets:
        if bullet.x < 1280 and bullet.x > 0:
            pass
        else:
            bullets.pop(bullets.index(bullet))
        if bullet.y < 960 and bullet.y > 0:
            bullet.y += bullet.speed
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        current_time = pygame.time.get_ticks()
        # задержка стрельбы по времени
        if current_time - prev_time > 200:
            prev_time = current_time
            bullets.append(Projectile(
                round(player.x + player.width // 2), round(player.y), 3, (255, 255, 224), 18, -1))

    if keys[pygame.K_LEFT] or keys[ord('a')]:
        player.x -= player.speed

    if keys[pygame.K_RIGHT] or keys[ord('d')]:
        player.x += player.speed

    if keys[pygame.K_UP] or keys[ord('w')]:
        player.y -= player.speed

    if keys[pygame.K_DOWN] or keys[ord('s')]:
        player.y += player.speed

    redrawGameWindow()

pygame.quit()
