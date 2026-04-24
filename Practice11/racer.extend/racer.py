import pygame
import random
import sys
import os

pygame.init() #zapusk pygame
pygame.mixer.init() #zapusk zvuka

# -----------------------------
# WINDOW
# -----------------------------
WIDTH = 500
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()
FPS = 120

# -----------------------------
# PATHS
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

# -----------------------------
# ROAD LIMITS
# -----------------------------
ROAD_LEFT = 120
ROAD_RIGHT = 380

lanes = [
    ROAD_LEFT + 40,
    (ROAD_LEFT + ROAD_RIGHT) // 2,
    ROAD_RIGHT - 40
]

# -----------------------------
# LEVELS
# -----------------------------
levels = {
    "easy": {
        "road_speed": 220,
        "player_speed": 340,
        "enemy_min": 250,
        "enemy_max": 350
    },
    "medium": {
        "road_speed": 300,
        "player_speed": 420,
        "enemy_min": 350,
        "enemy_max": 500
    },
    "hard": {
        "road_speed": 380,
        "player_speed": 500,
        "enemy_min": 500,
        "enemy_max": 700
    }
}

level_names = ["easy", "medium", "hard"]
selected_level_index = 0
current_level = level_names[selected_level_index]

# -----------------------------
# MENU / GARAGE
# -----------------------------
game_state = "menu"   # menu / garage / playing
menu_options = ["PLAY", "GARAGE", "EXIT"]
selected_menu_index = 0
garage_index = 0

# -----------------------------
# BEST SCORE SAVE
# -----------------------------
best_score_file = os.path.join(BASE_DIR, "best_score.txt")

def load_best_score():
    if os.path.exists(best_score_file):
        try:
            with open(best_score_file, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def save_best_score(score):
    with open(best_score_file, "w") as f:
        f.write(str(score))

best_score = load_best_score()

# -----------------------------
# LOAD SOUNDS
# -----------------------------
menu_music_path = os.path.join(SOUNDS_DIR, "menu.mp3")
game_music_path = os.path.join(SOUNDS_DIR, "background.mp3")

crash_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "crash.mp3"))
coin_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "coin.mp3"))

crash_sound.set_volume(0.7)
coin_sound.set_volume(0.7)
pygame.mixer.music.set_volume(0.4)

def play_menu_music():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(menu_music_path)
    pygame.mixer.music.play(-1)

def play_game_music():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(game_music_path)
    pygame.mixer.music.play(-1)

# -----------------------------
# LOAD IMAGES
# -----------------------------
road_img = pygame.image.load(os.path.join(IMAGES_DIR, "Road.jpg")).convert()
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

# player skins
player_skins = []
player_skin_files = [
    "main_car.jpg",
    "NPC1.jpg",
    "NPC2.jpg",
    "NPC3.jpg"
]

for skin_file in player_skin_files:
    img = pygame.image.load(os.path.join(IMAGES_DIR, skin_file)).convert_alpha()
    img = pygame.transform.scale(img, (40, 70))
    player_skins.append(img)

# npc cars
npc_images = []
for i in range(1, 10):
    img = pygame.image.load(os.path.join(IMAGES_DIR, f"NPC{i}.jpg")).convert_alpha()
    img = pygame.transform.scale(img, (40, 70))
    npc_images.append(img)

# coins
coin_images = {
    1: pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGES_DIR, "1coin.jpg")).convert_alpha(), (25, 25)
    ),
    3: pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGES_DIR, "3coin.jpg")).convert_alpha(), (25, 25)
    ),
    5: pygame.transform.scale(
        pygame.image.load(os.path.join(IMAGES_DIR, "5coin.jpg")).convert_alpha(), (25, 25)
    ),
}

# -----------------------------
# COIN CHANCE
# -----------------------------
def get_random_coin():
    roll = random.randint(1, 100)
    if roll <= 75:
        return 1   # gray
    elif roll <= 95:
        return 3   # gold
    else:
        return 5   # red

# -----------------------------
# SAFE SPAWN
# -----------------------------
def is_safe_position(x, y, enemies, min_dist=120):
    for e in enemies:
        if abs(e["y"] - y) < min_dist and abs(e["x"] - x) < 10:
            return False
    return True

# -----------------------------
# CREATE ENEMY
# -----------------------------
def create_enemy(level_name):
    level = levels[level_name]
    return {
        "img": random.choice(npc_images),
        "x": random.choice(lanes) - 20,
        "y": random.randint(-800, -100),
        "target_lane": None,
        "current_speed": 0,
        "max_speed": random.uniform(level["enemy_min"], level["enemy_max"]),
        "acceleration": random.uniform(1.5, 2.5)
    }

# -----------------------------
# RESPAWN COIN
# -----------------------------
def respawn_coin(state):
    while True:
        new_x = random.choice(lanes) - 12
        new_y = random.randint(-300, -100)

        safe = True
        for e in state["enemies"]:
            if abs(e["y"] - new_y) < 80 and abs(e["x"] - new_x) < 20:
                safe = False
                break

        if safe:
            state["coin_x"] = new_x
            state["coin_y"] = new_y
            state["coin_value"] = get_random_coin()
            break

# -----------------------------
# RESET GAME
# -----------------------------
def reset_game(level_name):
    enemies = []

    for _ in range(4):
        while True:
            e = create_enemy(level_name)
            if is_safe_position(e["x"], e["y"], enemies):
                enemies.append(e)
                break

    return {
        "player_x": lanes[1] - 20,
        "player_y": HEIGHT - 100,

        "enemies": enemies,

        "coin_value": get_random_coin(),
        "coin_x": random.choice(lanes) - 12,
        "coin_y": -200,
        "coin_speed": 5,

        "road_y1": 0.0,
        "road_y2": -HEIGHT,

        "coins": 0,
        "score": 0,
        "game_over": False,
        "level": level_name,
        "skin_index": garage_index,
        "speed": 0
    }

state = None

font = pygame.font.SysFont("Arial", 24)
game_over_font = pygame.font.SysFont("Arial", 40)
title_font = pygame.font.SysFont("Arial", 50)
menu_font = pygame.font.SysFont("Arial", 32)
small_font = pygame.font.SysFont("Arial", 22)

def update_best_score():
    global best_score, state
    if state["score"] > best_score:
        best_score = state["score"]
        save_best_score(best_score)

# =====================================
# LOOP
# =====================================
play_menu_music()
running = True

while running:
    dt = clock.tick(FPS) / 2000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_state == "menu":
                if event.key == pygame.K_UP:
                    selected_menu_index = (selected_menu_index - 1) % len(menu_options)

                elif event.key == pygame.K_DOWN:
                    selected_menu_index = (selected_menu_index + 1) % len(menu_options)

                elif event.key == pygame.K_LEFT:
                    if menu_options[selected_menu_index] == "PLAY":
                        selected_level_index = (selected_level_index - 1) % len(level_names)
                        current_level = level_names[selected_level_index]

                elif event.key == pygame.K_RIGHT:
                    if menu_options[selected_menu_index] == "PLAY":
                        selected_level_index = (selected_level_index + 1) % len(level_names)
                        current_level = level_names[selected_level_index]

                elif event.key == pygame.K_RETURN:
                    selected_option = menu_options[selected_menu_index]

                    if selected_option == "PLAY":
                        state = reset_game(current_level)
                        game_state = "playing"
                        play_game_music()

                    elif selected_option == "GARAGE":
                        game_state = "garage"

                    elif selected_option == "EXIT":
                        running = False

            elif game_state == "garage":
                if event.key == pygame.K_LEFT:
                    garage_index = (garage_index - 1) % len(player_skins)

                elif event.key == pygame.K_RIGHT:
                    garage_index = (garage_index + 1) % len(player_skins)

                elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    game_state = "menu"

            elif game_state == "playing":
                if state["game_over"] and event.key == pygame.K_r:
                    state = reset_game(state["level"])
                    play_game_music()

                elif state["game_over"] and event.key == pygame.K_ESCAPE:
                    game_state = "menu"
                    state = None
                    play_menu_music()

    keys = pygame.key.get_pressed()

    if game_state == "playing" and not state["game_over"]:

        player_speed = levels[state["level"]]["player_speed"]
        road_base_speed = levels[state["level"]]["road_speed"]

        # GAS / BRAKE
        speed_multiplier = 1.0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            speed_multiplier = 1.45

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            speed_multiplier = 0.55

        road_base_speed *= speed_multiplier
        player_speed *= speed_multiplier
        state["speed"] = int(road_base_speed)

        # PLAYER MOVE
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            state["player_x"] -= player_speed * dt

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            state["player_x"] += player_speed * dt

        # ROAD LIMIT
        if state["player_x"] < ROAD_LEFT or state["player_x"] > ROAD_RIGHT - 40:
            crash_sound.play()
            pygame.mixer.music.stop()
            state["game_over"] = True
            update_best_score()

        # ROAD SCROLL
        road_speed = road_base_speed * dt
        state["road_y1"] += road_speed
        state["road_y2"] += road_speed

        if state["road_y1"] >= HEIGHT:
            state["road_y1"] = -HEIGHT
        if state["road_y2"] >= HEIGHT:
            state["road_y2"] = -HEIGHT

        # ENEMIES
        for enemy in state["enemies"]:
            target_speed = enemy["max_speed"] * speed_multiplier

            for other in state["enemies"]:
                if other == enemy:
                    continue

                same_lane = abs(enemy["x"] - other["x"]) < 5
                in_front = other["y"] > enemy["y"]
                close = other["y"] - enemy["y"] < 120

                if same_lane and in_front and close:
                    target_speed = other["current_speed"] * 0.8

                    if enemy["target_lane"] is None:
                        possible = [l for l in lanes if abs((l - 20) - enemy["x"]) > 5]

                        for lane in possible:
                            lane_x = lane - 20
                            free = True
                            for e in state["enemies"]:
                                if abs(e["x"] - lane_x) < 5 and abs(e["y"] - enemy["y"]) < 120:
                                    free = False
                                    break
                            if free:
                                enemy["target_lane"] = lane_x
                                break
                    break

            enemy["current_speed"] += (target_speed - enemy["current_speed"]) * enemy["acceleration"] * dt
            enemy["y"] += enemy["current_speed"] * dt

            if enemy["target_lane"] is not None:
                enemy["x"] += (enemy["target_lane"] - enemy["x"]) * 4 * dt
                if abs(enemy["target_lane"] - enemy["x"]) < 2:
                    enemy["target_lane"] = None

            if enemy["y"] > HEIGHT:
                while True:
                    new_enemy = create_enemy(state["level"])
                    if is_safe_position(new_enemy["x"], new_enemy["y"], state["enemies"]):
                        enemy.update(new_enemy)
                        state["score"] += 1
                        break

        # COIN
        state["coin_y"] += state["coin_speed"] * 60 * dt * speed_multiplier

        if state["coin_y"] > HEIGHT:
            respawn_coin(state)

        # COLLISIONS
        player_rect = pygame.Rect(state["player_x"], state["player_y"], 40, 70)

        for enemy in state["enemies"]:
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 40, 70)
            if player_rect.colliderect(enemy_rect):
                crash_sound.play()
                pygame.mixer.music.stop()
                state["game_over"] = True
                update_best_score()

        coin_rect = pygame.Rect(state["coin_x"], state["coin_y"], 25, 25)
        if player_rect.colliderect(coin_rect):
            coin_sound.play()
            state["coins"] += state["coin_value"]
            respawn_coin(state)

    # DRAW
    screen.fill((20, 20, 20))

    if game_state == "menu":
        title_text = title_font.render("RACER", True, (255, 255, 255))
        info_text = small_font.render("UP/DOWN - menu   LEFT/RIGHT - level   ENTER - choose", True, (180, 180, 180))
        level_info = small_font.render(f"Selected level: {current_level.upper()}", True, (220, 220, 220))
        best_menu_text = small_font.render(f"Best score: {best_score}", True, (220, 220, 220))

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 120))

        for i, option in enumerate(menu_options):
            color = (255, 255, 0) if i == selected_menu_index else (255, 255, 255)
            option_text = menu_font.render(option, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, 260 + i * 70))

        screen.blit(level_info, (WIDTH // 2 - level_info.get_width() // 2, 500))
        screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, 560))
        screen.blit(best_menu_text, (WIDTH // 2 - best_menu_text.get_width() // 2, 620))

    elif game_state == "garage":
        garage_title = title_font.render("GARAGE", True, (255, 255, 255))
        garage_info = small_font.render("LEFT/RIGHT - change skin   ENTER/ESC - back", True, (200, 200, 200))
        skin_name = small_font.render(f"Skin {garage_index + 1}", True, (255, 255, 0))

        screen.blit(garage_title, (WIDTH // 2 - garage_title.get_width() // 2, 120))
        screen.blit(player_skins[garage_index], (WIDTH // 2 - 20, HEIGHT // 2 - 35))
        screen.blit(skin_name, (WIDTH // 2 - skin_name.get_width() // 2, HEIGHT // 2 + 70))
        screen.blit(garage_info, (WIDTH // 2 - garage_info.get_width() // 2, 620))

    elif game_state == "playing":
        screen.blit(road_img, (0, int(state["road_y1"])))
        screen.blit(road_img, (0, int(state["road_y2"])))

        screen.blit(player_skins[state["skin_index"]], (state["player_x"], state["player_y"]))

        for enemy in state["enemies"]:
            screen.blit(enemy["img"], (enemy["x"], enemy["y"]))

        coin_img = coin_images[state["coin_value"]]
        screen.blit(coin_img, (state["coin_x"], state["coin_y"]))

        # UI
        score_text = font.render(f"Score: {state['score']}", True, (255, 255, 255))
        coins_text = font.render(f"Coins: {state['coins']}", True, (255, 255, 255))
        level_text = font.render(f"Level: {state['level'].upper()}", True, (255, 255, 255))
        speed_text = font.render(f"Speed: {state['speed']}", True, (255, 255, 255))
        best_text = font.render(f"Best: {best_score}", True, (255, 255, 255))

        screen.blit(score_text, (10, 10))
        screen.blit(coins_text, (WIDTH - coins_text.get_width() - 10, 10))
        screen.blit(level_text, (10, 45))
        screen.blit(speed_text, (10, 80))
        screen.blit(best_text, (WIDTH - best_text.get_width() - 10, 45))

        if state["game_over"]:
            text1 = game_over_font.render("GAME OVER", True, (255, 0, 0))
            text2 = small_font.render("Press R to restart", True, (255, 255, 255))
            text3 = small_font.render("Press ESC for menu", True, (255, 255, 255))

            screen.blit(text1, (
                WIDTH // 2 - text1.get_width() // 2,
                HEIGHT // 2 - 60
            ))
            screen.blit(text2, (
                WIDTH // 2 - text2.get_width() // 2,
                HEIGHT // 2
            ))
            screen.blit(text3, (
                WIDTH // 2 - text3.get_width() // 2,
                HEIGHT // 2 + 35
            ))

    pygame.display.update()

pygame.quit()
sys.exit()