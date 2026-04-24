import pygame
import random
import sys

# -------------------- SETTINGS --------------------
CELL = 20
COLS = 30
ROWS = 20

WIDTH = COLS * CELL
HEIGHT = ROWS * CELL

FPS = 8

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 0, 0)
YELLOW = (255, 215, 0)
BLUE = (50, 150, 255)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)

# -------------------- INIT --------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# -------------------- FOOD TYPES --------------------
# Each type of food has:
# score -> how many points it gives
# color -> food color
# time  -> how long this food stays on screen (milliseconds)
FOOD_TYPES = [
    {"score": 1, "color": RED, "time": 7000},
    {"score": 2, "color": YELLOW, "time": 5000},
    {"score": 3, "color": BLUE, "time": 3000},
]


# -------------------- FUNCTIONS --------------------
def draw_grid():
    """Draw grid lines on the playing field."""
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def draw_text(text, x, y, color=WHITE):
    """Draw text on the screen."""
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def random_food_position(snake):
    """
    Generate a random position for food.
    Food must not appear inside the snake.
    """
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in snake:
            return pos


def generate_food(snake):
    """
    Create a new food object with:
    - random type
    - random position
    - spawn time for timer
    """
    food_type = random.choice(FOOD_TYPES)
    return {
        "pos": random_food_position(snake),
        "score": food_type["score"],
        "color": food_type["color"],
        "time": food_type["time"],
        "spawn_time": pygame.time.get_ticks()
    }


def game_over(score):
    """Show game over screen."""
    screen.fill(BLACK)
    draw_text("GAME OVER", WIDTH // 2 - 80, HEIGHT // 2 - 40, RED)
    draw_text(f"Score: {score}", WIDTH // 2 - 50, HEIGHT // 2)
    draw_text("Press any key to exit", WIDTH // 2 - 100, HEIGHT // 2 + 40)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


# -------------------- MAIN GAME --------------------
def main():
    # Initial snake body
    snake = [(5, 5), (4, 5), (3, 5)]

    # Initial direction: moving right
    dx, dy = 1, 0

    # Create first food
    food = generate_food(snake)

    score = 0
    running = True

    while running:
        # -------------------- EVENTS --------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Change direction with arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, 1
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = 1, 0

        # -------------------- FOOD TIMER --------------------
        # If food is not eaten in time, replace it
        current_time = pygame.time.get_ticks()
        if current_time - food["spawn_time"] > food["time"]:
            food = generate_food(snake)

        # -------------------- MOVE SNAKE --------------------
        head_x, head_y = snake[0]

        # Classic snake border wrap:
        # if snake leaves one side, it appears on the opposite side
        new_head = (
            (head_x + dx) % COLS,
            (head_y + dy) % ROWS
        )

        # -------------------- SELF COLLISION --------------------
        # Game over if snake hits itself
        if new_head in snake:
            game_over(score)
            return

        # Add new head
        snake.insert(0, new_head)

        # -------------------- FOOD CHECK --------------------
        if new_head == food["pos"]:
            # Add score depending on food weight
            score += food["score"]

            # Generate new food
            food = generate_food(snake)
        else:
            # If food was not eaten, remove tail
            snake.pop()

        # -------------------- DRAW --------------------
        screen.fill(BLACK)
        draw_grid()

        # Draw snake head
        pygame.draw.rect(
            screen,
            GREEN,
            (snake[0][0] * CELL, snake[0][1] * CELL, CELL, CELL)
        )

        # Draw snake body
        for part in snake[1:]:
            pygame.draw.rect(
                screen,
                DARK_GREEN,
                (part[0] * CELL, part[1] * CELL, CELL, CELL)
            )

        # Draw food
        pygame.draw.rect(
            screen,
            food["color"],
            (food["pos"][0] * CELL, food["pos"][1] * CELL, CELL, CELL)
        )

        # Draw score
        draw_text(f"Score: {score}", 10, 10)

        # Draw food weight
        draw_text(f"Food weight: {food['score']}", 10, 40)

        # Draw remaining timer
        remaining = max(0, (food["time"] - (current_time - food["spawn_time"])) // 1000)
        draw_text(f"Timer: {remaining}", 10, 70)

        pygame.display.flip()
        clock.tick(FPS)


# -------------------- START --------------------
main()
pygame.quit()