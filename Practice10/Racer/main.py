# Car Dodge Game with Coins + Sounds
# -----------------------------------------

import pygame
import random
import sys

# Initialize pygame
pygame.init()
pygame.mixer.init()

# -------------------------------
# SOUNDS
# -------------------------------
crash_sound = pygame.mixer.Sound("crash.mp3")
coin_sound = pygame.mixer.Sound("coin.mp3")

# -------------------------------
# WINDOW SETTINGS
# -------------------------------
WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Dodge Game with Coins")

FPS = 60
clock = pygame.time.Clock()

# -------------------------------
# COLORS
# -------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
RED = (255, 0, 0)
YELLOW = (255, 215, 0)
GRAY = (180, 180, 180)

# -------------------------------
# FONT
# -------------------------------
font = pygame.font.SysFont("Arial", 28)

# -------------------------------
# PLAYER
# -------------------------------
player_width = 50
player_height = 80
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 100
player_speed = 6

# -------------------------------
# ENEMY
# -------------------------------
enemy_width = 50
enemy_height = 80
enemy_x = random.randint(0, WIDTH - enemy_width)
enemy_y = -100
enemy_speed = 5

# -------------------------------
# COIN
# -------------------------------
coin_size = 20
coin_x = random.randint(0, WIDTH - coin_size)
coin_y = -300
coin_speed = 5

coins_collected = 0
score = 0

running = True

# =========================================
# MAIN LOOP
# =========================================
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -------------------------------
    # CONTROLS
    # -------------------------------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed

    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # -------------------------------
    # ENEMY MOVEMENT
    # -------------------------------
    enemy_y += enemy_speed

    if enemy_y > HEIGHT:
        enemy_y = -100
        enemy_x = random.randint(0, WIDTH - enemy_width)
        score += 1
        enemy_speed += 0.2

    # -------------------------------
    # COIN MOVEMENT
    # -------------------------------
    coin_y += coin_speed

    if coin_y > HEIGHT:
        coin_y = random.randint(-400, -100)
        coin_x = random.randint(0, WIDTH - coin_size)

    # -------------------------------
    # RECTANGLES
    # -------------------------------
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    coin_rect = pygame.Rect(coin_x, coin_y, coin_size, coin_size)

    # -------------------------------
    # COLLISION: ENEMY
    # -------------------------------
    if player_rect.colliderect(enemy_rect):
        crash_sound.play()
        pygame.time.delay(500)
        running = False

    # -------------------------------
    # COLLISION: COIN
    # -------------------------------
    if player_rect.colliderect(coin_rect):
        coin_sound.play()   # 🪙 sound
        coins_collected += 1
        coin_y = random.randint(-400, -100)
        coin_x = random.randint(0, WIDTH - coin_size)

    # -------------------------------
    # DRAW EVERYTHING
    # -------------------------------
    screen.fill(WHITE)

    pygame.draw.line(screen, GRAY, (130, 0), (130, HEIGHT), 4)
    pygame.draw.line(screen, GRAY, (270, 0), (270, HEIGHT), 4)

    pygame.draw.rect(screen, BLUE, player_rect)
    pygame.draw.rect(screen, RED, enemy_rect)

    pygame.draw.circle(screen, YELLOW,
                       (coin_x + coin_size // 2,
                        coin_y + coin_size // 2),
                       coin_size // 2)

    # SCORE
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    # COINS
    coin_text = font.render("Coins: " + str(coins_collected), True, BLACK)
    screen.blit(coin_text, (WIDTH - coin_text.get_width() - 10, 10))

    pygame.display.update()

# EXIT
pygame.quit()
sys.exit()