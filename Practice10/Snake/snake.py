import pygame
import random
import sys

# -------------------- SETTINGS --------------------
CELL_SIZE = 20
COLS = 30
ROWS = 20

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 0, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (50, 150, 255)

# Game settings
INITIAL_SPEED = 7          # speed at level 1
FOODS_PER_LEVEL = 4        # every 4 foods -> next level

# -------------------- INIT --------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake with Levels")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 26)
small_font = pygame.font.SysFont("Arial", 20)

# -------------------- WALLS --------------------
# Example walls inside the playing field
# You can change these coordinates if you want
walls = set()

# Horizontal wall
for x in range(8, 14):
    walls.add((x, 7))

# Vertical wall
for y in range(10, 15):
    walls.add((18, y))


# -------------------- FUNCTIONS --------------------
def draw_text(text, font_obj, color, x, y):
    """Draw text on the screen."""
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))


def generate_food(snake, walls):
    """
    Generate food at a random position.
    Food must not appear on the snake or on walls.
    """
    while True:
        food = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if food not in snake and food not in walls:
            return food


def draw_cell(position, color):
    """Draw one square cell."""
    rect = pygame.Rect(position[0] * CELL_SIZE, position[1] * CELL_SIZE,
                       CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)


def game_over_screen(score, level):
    """Show game over message."""
    screen.fill(BLACK)
    draw_text("GAME OVER", font, RED, WIDTH // 2 - 80, HEIGHT // 2 - 60)
    draw_text(f"Score: {score}", small_font, WHITE, WIDTH // 2 - 45, HEIGHT // 2 - 20)
    draw_text(f"Level: {level}", small_font, WHITE, WIDTH // 2 - 40, HEIGHT // 2 + 10)
    draw_text("Press R to restart or Q to quit", small_font, GRAY, WIDTH // 2 - 130, HEIGHT // 2 + 50)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def main():
    # Initial snake body
    snake = [(5, 5), (4, 5), (3, 5)]
    direction = (1, 0)      # moving right
    next_direction = direction

    food = generate_food(snake, walls)

    score = 0
    level = 1
    speed = INITIAL_SPEED

    running = True
    while running:
        # -------------------- EVENTS --------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Control snake direction
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    next_direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    next_direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_direction = (1, 0)

        direction = next_direction

        # -------------------- MOVE SNAKE --------------------
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        # -------------------- COLLISIONS --------------------
        # 1. Check if snake leaves the playing field
        if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
            game_over_screen(score, level)
            return

        # 2. Check collision with itself
        if new_head in snake:
            game_over_screen(score, level)
            return

        # 3. Check collision with walls
        if new_head in walls:
            game_over_screen(score, level)
            return

        # Add new head
        snake.insert(0, new_head)

        # -------------------- FOOD --------------------
        if new_head == food:
            score += 1

            # Level up every FOODS_PER_LEVEL foods
            if score % FOODS_PER_LEVEL == 0:
                level += 1
                speed += 2   # increase snake speed
            food = generate_food(snake, walls)
        else:
            # If snake didn't eat food, remove tail
            snake.pop()

        # -------------------- DRAW --------------------
        screen.fill(BLACK)

        # Draw walls
        for wall in walls:
            draw_cell(wall, GRAY)

        # Draw snake head
        draw_cell(snake[0], GREEN)

        # Draw snake body
        for part in snake[1:]:
            draw_cell(part, DARK_GREEN)

        # Draw food
        draw_cell(food, RED)

        # Draw score and level
        draw_text(f"Score: {score}", small_font, WHITE, 10, 10)
        draw_text(f"Level: {level}", small_font, BLUE, 10, 35)

        pygame.display.flip()

        # Control game speed
        clock.tick(speed)


# -------------------- START GAME --------------------
while True:
    main()