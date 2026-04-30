# config.py

CELL = 20
COLS = 30
ROWS = 26
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL
FPS = 60
BASE_SNAKE_SPEED = 8
TITLE = "TSIS 4 Snake"

# PostgreSQL settings
DB_NAME = "tsis4"
DB_USER = "postgres"
DB_PASSWORD = ""   # write your pgAdmin password here if PostgreSQL asks for it
DB_HOST = "localhost"
DB_PORT = "5432"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
LIGHT_GRAY = (150, 150, 150)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 0, 0)
DARK_RED = (120, 0, 0)
YELLOW = (255, 215, 0)
BLUE = (50, 150, 255)
PURPLE = (180, 80, 255)
CYAN = (0, 220, 220)
ORANGE = (255, 140, 0)
BROWN = (110, 80, 55)

FOODS_PER_LEVEL = 4

FOOD_TYPES = [
    {"score": 1, "color": RED, "time": 7000},
    {"score": 2, "color": YELLOW, "time": 5000},
    {"score": 3, "color": BLUE, "time": 3000},
]

POWERUP_TYPES = {
    "speed": {"color": ORANGE, "duration": 5000, "field_time": 8000},
    "slow": {"color": CYAN, "duration": 5000, "field_time": 8000},
    "shield": {"color": PURPLE, "duration": None, "field_time": 8000},
}

DEFAULT_SETTINGS = {
    "snake_color": [0, 200, 0],
    "grid": True,
    "sound": True,
}

SNAKE_COLORS = [
    [0, 200, 0], [40, 180, 255], [255, 120, 40],
    [180, 80, 255], [255, 70, 110], [255, 215, 0],
    [0, 220, 180], [255, 255, 255], [80, 255, 80],
    [255, 150, 200], [140, 220, 60], [80, 120, 255],
]
