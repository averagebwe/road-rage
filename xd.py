import os
import sys
import random
import pygame
import pygame_gui
import math


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

char = [load_image('player1.png'), load_image(
    'player2.png'), load_image('player3.png')]
bg = load_image('road.jpg')
scroll = bg.get_height()
tiles = math.ceil(WINDOW_HEIGHT / bg.get_height()) + 1

clock = pygame.time.Clock()

score = 0

bulletSound = pygame.mixer.Sound('data/shot.mp3')
explosionSound = pygame.mixer.Sound('data/kill.mp3')

ingameMusic = pygame.mixer.music.load('data/notmine_level_theme.mp3')
pygame.mixer.music.play(-1)


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7
        self.rideCount = 0
        self.hitbox = (self.x, self.y, 30, 30)
        self.health = 15
        self.visible = True
        self.alive = 1

    def draw(self, screen):
        if self.visible:
            if self.rideCount + 1 >= 15:
                self.rideCount = 0
            screen.blit(char[self.rideCount // 5], (self.x, self.y))
            self.rideCount += 1
            self.hitbox = (self.x, self.y, 30, 30)
            pygame.draw.rect(screen, (255, 0, 0),
                             (self.hitbox[0], self.hitbox[1] - 20, 30, 5))
            pygame.draw.rect(screen, (0, 255, 0),
                             (self.hitbox[0], self.hitbox[1] - 20, 30 - ((30 / 15) * (15 - self.health)), 5))
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.death()

    def death(self):
        if self.alive == 1:
            explosionSound.play()
            self.alive = 0
        self.visible = False


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
        self.hitbox = (self.x, self.y, 50, 50)
        self.health = 8

    def draw(self, screen):
        self.move()
        self.shoot()
        if self.rideCount + 1 >= 9:
            self.rideCount = 0
        screen.blit(self.en[self.rideCount // 3], (self.x, self.y))
        self.rideCount += 1
        self.hitbox = (self.x, self.y, 50, 50)

        pygame.draw.rect(screen, (255, 0, 0),
                         (self.hitbox[0], self.hitbox[1] - 20, 50, 5))
        pygame.draw.rect(screen, (0, 255, 0),
                         (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50 / 8) * (8 - self.health)), 5))
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.y + self.speed < self.path[1]:
            self.y += self.speed
        else:
            self.speed = 0

    def shoot(self):
        if self.speed == 0:
            if random.randrange(0, self.velocity * FPS) == 1:
                enemy_bullets.append(Projectile(
                    round(self.x + self.width // 2), round(self.y + self.height), 3, (255, 255, 225), 14, 1))
                bulletSound.play()

    def hit(self):
        global score
        if self.health > 0:
            self.health -= 1
        else:
            explosionSound.play()
            enemies.pop(enemies.index(self))
            score += 1


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
    global scroll
    i = 0
    while (i < tiles):
        screen.blit(bg, (0, bg.get_height() * i - scroll))
        i += 1
    scroll -= 6
    if scroll < 0:
        scroll = bg.get_height()
    text = font.render('УНИЧТОЖЕНО: ' + str(score), 1, (255, 255, 255))
    screen.blit(text, (10, 10))
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for bullet in enemy_bullets:
        bullet.draw(screen)

    pygame.display.update()


font = pygame.font.Font('data/3712-font.otf', 30)
player = Player(WINDOW_WIDTH // 2, 900, 30, 30)
bullets = []
bullets_removed = set()
enemy_bullets = []
enemy_bullets_removed = set()
enemies = [Enemy(random.randrange(0, WINDOW_WIDTH - 50), 0, 50,
                 50, 4, random.randrange(50, WINDOW_HEIGHT - 500), 3) for _ in range(random.randrange(3, 11))]
prev_time = pygame.time.get_ticks()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if enemies == []:
        enemies = [Enemy(random.randrange(0, WINDOW_WIDTH - 50), 0, 50,
                         50, 4, random.randrange(50, WINDOW_HEIGHT - 500), 3) for _ in range(random.randrange(3, 11))]

    for enemy in enemies:
        if player.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and player.hitbox[1] + player.hitbox[3] > enemy.hitbox[1]:
            if player.hitbox[0] + player.hitbox[2] > enemy.hitbox[0] and player.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
                player.hit()
                enemy.health = 0
                enemy.hit()

    for bullet in bullets:
        for enemy in enemies:
            if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
                if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                    enemy.hit()
                    bullets_removed.add(bullet)
                    bullets = [
                        bullet for bullet in bullets if bullet not in bullets_removed]

        if bullet.x < 1280 and bullet.x > 0:
            pass
        else:
            bullets_removed.add(bullet)
            bullets = [
                bullet for bullet in bullets if bullet not in bullets_removed]
        if bullet.y < 960 and bullet.y > 0:
            bullet.y += bullet.speed
        else:
            bullets_removed.add(bullet)
            bullets = [
                bullet for bullet in bullets if bullet not in bullets_removed]

    for enemy_bullet in enemy_bullets:
        if enemy_bullet.y - enemy_bullet.radius < player.hitbox[1] + player.hitbox[3] and enemy_bullet.y + enemy_bullet.radius > player.hitbox[1]:
            if enemy_bullet.x + enemy_bullet.radius > player.hitbox[0] and enemy_bullet.x - enemy_bullet.radius < player.hitbox[0] + player.hitbox[2]:
                player.hit()
                enemy_bullets_removed.add(enemy_bullet)
                enemy_bullets = [
                    enemy_bullet for enemy_bullet in enemy_bullets if enemy_bullet not in enemy_bullets_removed]

        if enemy_bullet.x < 1280 and enemy_bullet.x > 0:
            pass
        else:
            enemy_bullets_removed.add(enemy_bullet)
            enemy_bullets = [
                enemy_bullet for enemy_bullet in enemy_bullets if enemy_bullet not in enemy_bullets_removed]
        if enemy_bullet.y < 960 and enemy_bullet.y > 0:
            enemy_bullet.y += enemy_bullet.speed
        else:
            enemy_bullets_removed.add(enemy_bullet)
            enemy_bullets = [
                enemy_bullet for enemy_bullet in enemy_bullets if enemy_bullet not in enemy_bullets_removed]

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if player.visible == True:
            current_time = pygame.time.get_ticks()
            # задержка стрельбы по времени
            if current_time - prev_time > 200:
                prev_time = current_time
                bullets.append(Projectile(
                    round(player.x + player.width // 2), round(player.y), 3, (255, 255, 224), 18, -1))
                bulletSound.play()

    if keys[pygame.K_LEFT] or keys[ord('a')] and player.x > player.speed:
        player.x -= player.speed

    if keys[pygame.K_RIGHT] or keys[ord('d')] and player.x < WINDOW_WIDTH - player.width - player.speed:
        player.x += player.speed

    if keys[pygame.K_UP] or keys[ord('w')] and player.y > player.speed:
        player.y -= player.speed

    if keys[pygame.K_DOWN] or keys[ord('s')] and player.y < WINDOW_HEIGHT - player.height - player.speed:
        player.y += player.speed

    redrawGameWindow()

pygame.quit()
