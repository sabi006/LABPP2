# Car Dodge Game with Coins
# -----------------------------------------
# Controls:
# Left Arrow  -> move left
# Right Arrow -> move right
#
# Goal:
# Avoid enemy cars and collect coins.
# -----------------------------------------

import pygame
import random
import sys

# Initialize pygame
pygame.init()

# -------------------------------
# WINDOW SETTINGS
# -------------------------------
WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Dodge Game with Coins")

# Frames per second
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
# PLAYER SETTINGS
# -------------------------------
player_width = 50
player_height = 80

player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 100

player_speed = 6

# -------------------------------
# ENEMY SETTINGS
# -------------------------------
enemy_width = 50
enemy_height = 80

enemy_x = random.randint(0, WIDTH - enemy_width)
enemy_y = -100

enemy_speed = 5

# -------------------------------
# COIN SETTINGS
# -------------------------------
coin_size = 20

# Coin starts above the screen
coin_x = random.randint(0, WIDTH - coin_size)
coin_y = -300

coin_speed = 5

# Number of collected coins
coins_collected = 0

# -------------------------------
# SCORE
# -------------------------------
score = 0

# -------------------------------
# GAME LOOP CONTROL
# -------------------------------
running = True

# =========================================
# MAIN GAME LOOP
# =========================================
while running:

    # Control FPS
    clock.tick(FPS)

    # -------------------------------
    # EVENTS
    # -------------------------------
    for event in pygame.event.get():

        # Close window
        if event.type == pygame.QUIT:
            running = False

    # -------------------------------
    # KEYBOARD INPUT
    # -------------------------------
    keys = pygame.key.get_pressed()

    # Move left
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed

    # Move right
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # -------------------------------
    # ENEMY MOVEMENT
    # -------------------------------
    enemy_y += enemy_speed

    # If enemy leaves screen, respawn
    if enemy_y > HEIGHT:
        enemy_y = -100
        enemy_x = random.randint(0, WIDTH - enemy_width)

        score += 1
        enemy_speed += 0.2   # increase difficulty

    # -------------------------------
    # COIN MOVEMENT
    # -------------------------------
    coin_y += coin_speed

    # If coin leaves screen, respawn randomly
    if coin_y > HEIGHT:
        coin_y = random.randint(-400, -100)
        coin_x = random.randint(0, WIDTH - coin_size)

    # -------------------------------
    # RECTANGLES FOR COLLISION
    # -------------------------------
    player_rect = pygame.Rect(player_x, player_y,
                              player_width, player_height)

    enemy_rect = pygame.Rect(enemy_x, enemy_y,
                             enemy_width, enemy_height)

    coin_rect = pygame.Rect(coin_x, coin_y,
                            coin_size, coin_size)

    # -------------------------------
    # COLLISION: PLAYER + ENEMY
    # -------------------------------
    if player_rect.colliderect(enemy_rect):
        running = False

    # -------------------------------
    # COLLISION: PLAYER + COIN
    # -------------------------------
    if player_rect.colliderect(coin_rect):

        # Add one collected coin
        coins_collected += 1

        # Respawn coin randomly
        coin_y = random.randint(-400, -100)
        coin_x = random.randint(0, WIDTH - coin_size)

    # -------------------------------
    # DRAW EVERYTHING
    # -------------------------------
    screen.fill(WHITE)

    # Road lines
    pygame.draw.line(screen, GRAY, (130, 0), (130, HEIGHT), 4)
    pygame.draw.line(screen, GRAY, (270, 0), (270, HEIGHT), 4)

    # Draw player car
    pygame.draw.rect(screen, BLUE, player_rect)

    # Draw enemy car
    pygame.draw.rect(screen, RED, enemy_rect)

    # Draw coin
    pygame.draw.circle(screen, YELLOW,
                       (coin_x + coin_size // 2,
                        coin_y + coin_size // 2),
                       coin_size // 2)

    # -------------------------------
    # TEXT: SCORE (top left)
    # -------------------------------
    score_text = font.render("Score: " + str(score),
                             True, BLACK)
    screen.blit(score_text, (10, 10))

    # -------------------------------
    # TEXT: COINS (top right)
    # -------------------------------
    coin_text = font.render("Coins: " + str(coins_collected),
                            True, BLACK)

    # Place in top right corner
    screen.blit(coin_text,
                (WIDTH - coin_text.get_width() - 10, 10))

    # Update screen
    pygame.display.update()

# -----------------------------------------
# EXIT GAME
# -----------------------------------------
pygame.quit()
sys.exit()