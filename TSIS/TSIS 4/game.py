# game.py
import json
import os
import random
import sys

import pygame

from config import *
from db import save_result, get_top_10, get_personal_best


class SnakeGame:
    def __init__(self):
        pygame.init()

        try:
            pygame.mixer.init()
            self.audio_available = True
        except pygame.error:
            self.audio_available = False

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.big_font = pygame.font.SysFont("Arial", 42, bold=True)
        self.medium_font = pygame.font.SysFont("Arial", 28, bold=True)

        self.settings = self.load_settings()
        self.username = ""
        self.personal_best = 0
        self.state = "menu"
        self.final_score = 0
        self.final_level = 1
        self.game_saved = False

        self.apple_image = None
        self.sounds = {}
        self.load_assets()

        self.color_page = 0
        self.colors_per_page = 6

        self.reset_game()

    def load_settings(self):
        if not os.path.exists("settings.json"):
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(DEFAULT_SETTINGS, f, indent=4)
            return DEFAULT_SETTINGS.copy()

        with open("settings.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for key, value in DEFAULT_SETTINGS.items():
            data.setdefault(key, value)
        return data

    def save_settings(self):
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def load_assets(self):
        apple_path = os.path.join("assets", "images", "apple.png")
        if os.path.exists(apple_path):
            try:
                img = pygame.image.load(apple_path).convert_alpha()
                self.apple_image = pygame.transform.scale(img, (CELL, CELL))
            except pygame.error:
                self.apple_image = None

        self.sounds = {
            "eat": self.load_sound("eat", fallback="ear"),
            "poison": self.load_sound("poison"),
            "powerup": self.load_sound("powerup"),
            "gameover": self.load_sound("gameover"),
        }

    def load_sound(self, name, fallback=None):
        if not self.audio_available:
            return None

        names = [name]
        if fallback:
            names.append(fallback)

        for base in names:
            for ext in (".wav", ".mp3", ".ogg"):
                path = os.path.join("assets", "sounds", base + ext)
                if os.path.exists(path):
                    try:
                        return pygame.mixer.Sound(path)
                    except pygame.error:
                        pass
        return None

    def play_sound(self, name):
        if self.settings.get("sound", True):
            sound = self.sounds.get(name)
            if sound:
                sound.play()

    def draw_text(self, text, x, y, color=WHITE, center=False, font=None):
        font = font or self.font
        surf = font.render(str(text), True, color)
        rect = surf.get_rect()

        if center:
            rect.center = (x, y)
            self.screen.blit(surf, rect)
        else:
            self.screen.blit(surf, (x, y))

    def draw_button(self, rect, text, color=(75, 115, 65)):
        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=12)
        self.draw_text(text, rect.centerx, rect.centery, WHITE, center=True, font=self.small_font)

    def draw_background(self):
        c1 = (170, 215, 81)
        c2 = (162, 209, 73)

        for row in range(ROWS):
            for col in range(COLS):
                color = c1 if (row + col) % 2 == 0 else c2
                pygame.draw.rect(self.screen, color, (col * CELL, row * CELL, CELL, CELL))

    def draw_grid(self):
        if not self.settings.get("grid", True):
            return

        for x in range(0, WIDTH, CELL):
            pygame.draw.line(self.screen, (140, 190, 70), (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(self.screen, (140, 190, 70), (0, y), (WIDTH, y))

    def reset_game(self):
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.dx, self.dy = 1, 0

        self.score = 0
        self.level = 1
        self.food_eaten = 0

        self.current_speed = BASE_SNAKE_SPEED
        self.max_speed = 14
        self.move_delay = 1000 / self.current_speed
        self.last_move_time = pygame.time.get_ticks()

        self.obstacles = set()
        self.food = None
        self.poison_food = None
        self.powerup = None
        self.last_powerup_spawn = pygame.time.get_ticks()

        self.shield = False
        self.active_effect = None
        self.effect_end_time = 0
        self.game_saved = False

        self.warning_text = ""
        self.warning_until = 0

        self.food = self.generate_food()
        self.poison_food = self.generate_poison_food()

    def occupied_positions(self):
        occupied = set(self.snake) | set(self.obstacles)

        if self.food:
            occupied.add(self.food["pos"])

        if self.poison_food:
            occupied.add(self.poison_food["pos"])

        if self.powerup:
            occupied.add(self.powerup["pos"])

        return occupied

    def random_free_position(self):
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in self.occupied_positions():
                return pos

    def generate_food(self):
        data = random.choice(FOOD_TYPES)

        return {
            "pos": self.random_free_position(),
            "score": data["score"],
            "color": data["color"],
            "time": data["time"],
            "spawn_time": pygame.time.get_ticks(),
        }

    def generate_poison_food(self):
        return {
            "pos": self.random_free_position(),
            "color": DARK_RED,
            "time": 6000,
            "spawn_time": pygame.time.get_ticks(),
        }

    def generate_powerup(self):
        kind = random.choice(list(POWERUP_TYPES.keys()))

        return {
            "type": kind,
            "pos": self.random_free_position(),
            "color": POWERUP_TYPES[kind]["color"],
            "field_time": POWERUP_TYPES[kind]["field_time"],
            "spawn_time": pygame.time.get_ticks(),
        }

    def apply_speed(self):
        speed = min(BASE_SNAKE_SPEED + (self.level - 1) * 0.6, self.max_speed)

        if self.active_effect == "speed":
            speed += 2
        elif self.active_effect == "slow":
            speed = max(4, speed - 2)

        self.current_speed = speed
        self.move_delay = 1000 / self.current_speed

    def count_free_neighbors(self, pos, obstacles):
        x, y = pos
        count = 0

        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                if (nx, ny) not in obstacles and (nx, ny) not in self.snake:
                    count += 1

        return count

    def generate_obstacles(self):
        head = self.snake[0]

        safe_zone = {
            head,
            (head[0] + 1, head[1]),
            (head[0] - 1, head[1]),
            (head[0], head[1] + 1),
            (head[0], head[1] - 1),
        }

        target = min(5 + self.level, 18)

        for _ in range(80):
            obstacles = set()
            attempts = 0

            while len(obstacles) < target and attempts < 1000:
                attempts += 1
                pos = (random.randint(1, COLS - 2), random.randint(1, ROWS - 2))

                if pos not in self.snake and pos not in safe_zone:
                    obstacles.add(pos)

            if self.count_free_neighbors(head, obstacles) >= 2:
                self.obstacles = obstacles
                break

        self.food = self.generate_food()
        self.poison_food = self.generate_poison_food()
        self.powerup = None

    def level_up(self):
        self.level += 1
        self.apply_speed()

        if self.level >= 3:
            self.generate_obstacles()

    def activate_powerup(self, kind):
        now = pygame.time.get_ticks()

        if kind in ("speed", "slow"):
            self.active_effect = kind
            self.effect_end_time = now + POWERUP_TYPES[kind]["duration"]
            self.apply_speed()

        elif kind == "shield":
            self.shield = True
            self.active_effect = "shield"
            self.effect_end_time = 0

    def update_effects(self):
        now = pygame.time.get_ticks()

        if self.active_effect in ("speed", "slow") and now >= self.effect_end_time:
            self.active_effect = None
            self.apply_speed()

    def trigger_game_over(self):
        self.final_score = self.score
        self.final_level = self.level
        self.play_sound("gameover")
        self.state = "game_over"

    def save_result_once(self):
        if not self.game_saved and self.username.strip():
            save_result(self.username.strip(), self.final_score, self.final_level)
            self.game_saved = True

    def draw_snake(self):
        snake_color = tuple(self.settings.get("snake_color", DEFAULT_SETTINGS["snake_color"]))

        outline = (
            max(0, snake_color[0] - 70),
            max(0, snake_color[1] - 70),
            max(0, snake_color[2] - 70),
        )

        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(x * CELL + 1, y * CELL + 1, CELL - 2, CELL - 2)
            pygame.draw.rect(self.screen, snake_color, rect, border_radius=7)
            pygame.draw.rect(self.screen, outline, rect, 2, border_radius=7)

            if i == 0:
                eye_color = BLACK if snake_color != BLACK else WHITE

                if self.dx == 1:
                    eyes = [(x * CELL + 13, y * CELL + 5), (x * CELL + 13, y * CELL + 14)]
                elif self.dx == -1:
                    eyes = [(x * CELL + 6, y * CELL + 5), (x * CELL + 6, y * CELL + 14)]
                elif self.dy == -1:
                    eyes = [(x * CELL + 5, y * CELL + 6), (x * CELL + 14, y * CELL + 6)]
                else:
                    eyes = [(x * CELL + 5, y * CELL + 13), (x * CELL + 14, y * CELL + 13)]

                for eye in eyes:
                    pygame.draw.circle(self.screen, eye_color, eye, 2)

    def draw_food(self):
        x, y = self.food["pos"]
        px, py = x * CELL, y * CELL

        if self.apple_image:
            self.screen.blit(self.apple_image, (px, py))
        else:
            pygame.draw.circle(
                self.screen,
                self.food["color"],
                (px + CELL // 2, py + CELL // 2),
                CELL // 2 - 2,
            )

    def draw_poison_food(self):
        x, y = self.poison_food["pos"]
        px, py = x * CELL, y * CELL

        pygame.draw.circle(self.screen, DARK_RED, (px + CELL // 2, py + CELL // 2), CELL // 2 - 2)
        pygame.draw.circle(self.screen, (180, 20, 20), (px + CELL // 2, py + CELL // 2), CELL // 2 - 6)
        self.draw_text("!", px + CELL // 2, py + CELL // 2, WHITE, center=True, font=self.small_font)

    def draw_powerup(self):
        if not self.powerup:
            return

        x, y = self.powerup["pos"]
        px, py = x * CELL, y * CELL

        pygame.draw.rect(
            self.screen,
            self.powerup["color"],
            (px + 2, py + 2, CELL - 4, CELL - 4),
            border_radius=6,
        )

        letter = {"speed": "S", "slow": "M", "shield": "H"}[self.powerup["type"]]
        self.draw_text(letter, px + CELL // 2, py + CELL // 2, WHITE, center=True, font=self.small_font)

    def draw_obstacles(self):
        for x, y in self.obstacles:
            rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
            pygame.draw.rect(self.screen, GRAY, rect, border_radius=4)
            pygame.draw.rect(self.screen, (55, 55, 55), rect.inflate(-4, -4), border_radius=4)

    def menu_screen(self):
        play_btn = pygame.Rect(WIDTH // 2 - 110, 200, 220, 55)
        leader_btn = pygame.Rect(WIDTH // 2 - 110, 265, 220, 55)
        settings_btn = pygame.Rect(WIDTH // 2 - 110, 330, 220, 55)
        quit_btn = pygame.Rect(WIDTH // 2 - 110, 395, 220, 55)
        username_box = pygame.Rect(WIDTH // 2 - 155, 125, 310, 48)

        while self.state == "menu":
            self.draw_background()

            self.draw_text("SNAKE", WIDTH // 2, 55, WHITE, center=True, font=self.big_font)
            self.draw_text("Enter username", WIDTH // 2, 100, WHITE, center=True, font=self.small_font)

            pygame.draw.rect(self.screen, (70, 110, 60), username_box, border_radius=12)
            pygame.draw.rect(self.screen, WHITE, username_box, 2, border_radius=12)

            shown_name = self.username if self.username else "type here..."
            self.draw_text(shown_name, username_box.x + 12, username_box.y + 12, WHITE, font=self.small_font)

            self.draw_button(play_btn, "Play")
            self.draw_button(leader_btn, "Leaderboard")
            self.draw_button(settings_btn, "Settings")
            self.draw_button(quit_btn, "Quit")

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif event.key == pygame.K_RETURN and self.username.strip():
                        self.personal_best = get_personal_best(self.username.strip())
                        self.reset_game()
                        self.state = "game"
                    elif len(self.username) < 15 and event.unicode.isprintable():
                        self.username += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos

                    if play_btn.collidepoint(pos) and self.username.strip():
                        self.personal_best = get_personal_best(self.username.strip())
                        self.reset_game()
                        self.state = "game"

                    elif leader_btn.collidepoint(pos):
                        self.state = "leaderboard"

                    elif settings_btn.collidepoint(pos):
                        self.state = "settings"

                    elif quit_btn.collidepoint(pos):
                        pygame.quit()
                        sys.exit()

            self.clock.tick(30)

    def leaderboard_screen(self):
        back_btn = pygame.Rect(WIDTH // 2 - 70, HEIGHT - 58, 140, 40)

        while self.state == "leaderboard":
            rows = get_top_10()

            self.screen.fill((30, 50, 25))
            self.draw_text("Leaderboard", WIDTH // 2, 40, YELLOW, center=True, font=self.big_font)

            self.draw_text("Rank", 40, 90, WHITE, font=self.small_font)
            self.draw_text("Username", 90, 90, WHITE, font=self.small_font)
            self.draw_text("Score", 240, 90, WHITE, font=self.small_font)
            self.draw_text("Level", 320, 90, WHITE, font=self.small_font)
            self.draw_text("Date", 395, 90, WHITE, font=self.small_font)

            y = 125

            for i, (username, score, level, played_at) in enumerate(rows, start=1):
                self.draw_text(i, 40, y, WHITE, font=self.small_font)
                self.draw_text(username, 90, y, WHITE, font=self.small_font)
                self.draw_text(score, 240, y, WHITE, font=self.small_font)
                self.draw_text(level, 320, y, WHITE, font=self.small_font)
                self.draw_text(played_at.strftime("%Y-%m-%d"), 395, y, WHITE, font=self.small_font)
                y += 31

            self.draw_button(back_btn, "Back")
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and back_btn.collidepoint(event.pos):
                    self.state = "menu"

            self.clock.tick(30)

    def settings_screen(self):
        grid_btn = pygame.Rect(60, 115, 220, 45)
        sound_btn = pygame.Rect(320, 115, 220, 45)
        prev_btn = pygame.Rect(110, 395, 100, 42)
        next_btn = pygame.Rect(390, 395, 100, 42)
        save_btn = pygame.Rect(WIDTH // 2 - 95, HEIGHT - 60, 190, 42)

        while self.state == "settings":
            self.screen.fill((30, 50, 25))

            self.draw_text("Settings", WIDTH // 2, 45, CYAN, center=True, font=self.big_font)
            self.draw_button(grid_btn, f"Grid: {'ON' if self.settings['grid'] else 'OFF'}")
            self.draw_button(sound_btn, f"Sound: {'ON' if self.settings['sound'] else 'OFF'}")
            self.draw_text("Snake color", WIDTH // 2, 195, WHITE, center=True, font=self.medium_font)

            start = self.color_page * self.colors_per_page
            page_colors = SNAKE_COLORS[start:start + self.colors_per_page]
            color_rects = []

            for idx, color in enumerate(page_colors):
                row = idx // 3
                col = idx % 3

                rect = pygame.Rect(120 + col * 130, 235 + row * 65, 70, 45)

                pygame.draw.rect(self.screen, tuple(color), rect, border_radius=10)
                pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=10)

                if self.settings["snake_color"] == color:
                    pygame.draw.rect(self.screen, YELLOW, rect.inflate(8, 8), 3, border_radius=12)

                color_rects.append((rect, color))

            max_page = (len(SNAKE_COLORS) - 1) // self.colors_per_page

            self.draw_button(prev_btn, "Prev", (60, 95, 60))
            self.draw_button(next_btn, "Next", (60, 95, 60))
            self.draw_text(f"Page {self.color_page + 1}/{max_page + 1}", WIDTH // 2, 418, WHITE, center=True, font=self.small_font)
            self.draw_button(save_btn, "Save & Back")

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos

                    if grid_btn.collidepoint(pos):
                        self.settings["grid"] = not self.settings["grid"]

                    elif sound_btn.collidepoint(pos):
                        self.settings["sound"] = not self.settings["sound"]

                    elif prev_btn.collidepoint(pos):
                        self.color_page = max(0, self.color_page - 1)

                    elif next_btn.collidepoint(pos):
                        self.color_page = min(max_page, self.color_page + 1)

                    elif save_btn.collidepoint(pos):
                        self.save_settings()
                        self.state = "menu"

                    else:
                        for rect, color in color_rects:
                            if rect.collidepoint(pos):
                                self.settings["snake_color"] = color

            self.clock.tick(30)

    def game_over_screen(self):
        self.save_result_once()

        current_best = get_personal_best(self.username.strip()) if self.username.strip() else 0

        retry_btn = pygame.Rect(WIDTH // 2 - 100, 280, 200, 45)
        menu_btn = pygame.Rect(WIDTH // 2 - 100, 340, 200, 45)

        while self.state == "game_over":
            self.screen.fill((30, 50, 25))

            self.draw_text("Game Over", WIDTH // 2, 85, RED, center=True, font=self.big_font)
            self.draw_text(f"Player: {self.username}", WIDTH // 2, 145, WHITE, center=True)
            self.draw_text(f"Score: {self.final_score}", WIDTH // 2, 180, WHITE, center=True)
            self.draw_text(f"Level reached: {self.final_level}", WIDTH // 2, 215, WHITE, center=True)
            self.draw_text(f"Best: {current_best}", WIDTH // 2, 250, YELLOW, center=True)

            self.draw_button(retry_btn, "Retry")
            self.draw_button(menu_btn, "Main Menu")

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_btn.collidepoint(event.pos):
                        self.personal_best = get_personal_best(self.username.strip())
                        self.reset_game()
                        self.state = "game"

                    elif menu_btn.collidepoint(event.pos):
                        self.state = "menu"

            self.clock.tick(30)

    def shield_protect(self):
        self.shield = False
        self.active_effect = None
        self.warning_text = "SHIELD SAVED YOU!"
        self.warning_until = pygame.time.get_ticks() + 1200

    def move_snake(self):
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.dx, head_y + self.dy)

        wall_hit = not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS)
        self_hit = new_head in self.snake
        obstacle_hit = new_head in self.obstacles

        if wall_hit:
            if self.shield:
                self.shield_protect()
                return

            self.warning_text = "WALL HIT!"
            self.warning_until = pygame.time.get_ticks() + 1000
            self.trigger_game_over()
            return

        if self_hit:
            if self.shield:
                self.shield_protect()
                return

            self.warning_text = "SELF COLLISION!"
            self.warning_until = pygame.time.get_ticks() + 1000
            self.trigger_game_over()
            return

        if obstacle_hit:
            self.warning_text = "OBSTACLE HIT!"
            self.warning_until = pygame.time.get_ticks() + 1000
            self.trigger_game_over()
            return

        self.snake.insert(0, new_head)
        grew = False

        if new_head == self.food["pos"]:
            self.score += self.food["score"]
            self.food_eaten += 1
            grew = True

            self.warning_text = f"+{self.food['score']} score"
            self.warning_until = pygame.time.get_ticks() + 900

            self.play_sound("eat")
            self.food = self.generate_food()

            if self.food_eaten % FOODS_PER_LEVEL == 0:
                self.level_up()

        elif new_head == self.poison_food["pos"]:
            self.score = max(0, self.score - 1)

            self.warning_text = "POISON! -1 score, -2 length"
            self.warning_until = pygame.time.get_ticks() + 1500

            self.play_sound("poison")
            self.poison_food = self.generate_poison_food()

            for _ in range(2):
                if self.snake:
                    self.snake.pop()

            if len(self.snake) <= 1:
                self.trigger_game_over()
                return

            grew = True

        elif self.powerup and new_head == self.powerup["pos"]:
            self.activate_powerup(self.powerup["type"])

            self.warning_text = f"POWER-UP: {self.powerup['type'].upper()}"
            self.warning_until = pygame.time.get_ticks() + 1200

            self.play_sound("powerup")
            self.powerup = None

        if not grew:
            self.snake.pop()

    def game_loop(self):
        while self.state == "game":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.dy == 0:
                        self.dx, self.dy = 0, -1
                    elif event.key == pygame.K_DOWN and self.dy == 0:
                        self.dx, self.dy = 0, 1
                    elif event.key == pygame.K_LEFT and self.dx == 0:
                        self.dx, self.dy = -1, 0
                    elif event.key == pygame.K_RIGHT and self.dx == 0:
                        self.dx, self.dy = 1, 0

            now = pygame.time.get_ticks()

            if now - self.food["spawn_time"] > self.food["time"]:
                self.food = self.generate_food()

            if now - self.poison_food["spawn_time"] > self.poison_food["time"]:
                self.poison_food = self.generate_poison_food()

            if self.powerup is None and now - self.last_powerup_spawn > 6000:
                self.powerup = self.generate_powerup()
                self.last_powerup_spawn = now

            if self.powerup and now - self.powerup["spawn_time"] > self.powerup["field_time"]:
                self.powerup = None

            self.update_effects()

            if now - self.last_move_time >= self.move_delay:
                self.last_move_time = now
                self.move_snake()

                if self.state != "game":
                    return

            self.draw_background()
            self.draw_grid()
            self.draw_obstacles()
            self.draw_food()
            self.draw_poison_food()
            self.draw_powerup()
            self.draw_snake()

            self.draw_text(f"Score: {self.score}", 10, 8, WHITE, font=self.small_font)
            self.draw_text(f"Level: {self.level}", 10, 30, WHITE, font=self.small_font)
            self.draw_text(f"Best: {self.personal_best}", 10, 52, YELLOW, font=self.small_font)

            if self.warning_text and pygame.time.get_ticks() < self.warning_until:
                self.draw_text(
                    self.warning_text,
                    WIDTH // 2,
                    85,
                    DARK_RED,
                    center=True,
                    font=self.medium_font,
                )

            if self.shield:
                self.draw_text("Shield", WIDTH - 90, 8, PURPLE, font=self.small_font)
            elif self.active_effect == "speed":
                self.draw_text("Speed", WIDTH - 90, 8, ORANGE, font=self.small_font)
            elif self.active_effect == "slow":
                self.draw_text("Slow", WIDTH - 90, 8, CYAN, font=self.small_font)

            pygame.display.flip()
            self.clock.tick(FPS)

    def run(self):
        while True:
            if self.state == "menu":
                self.menu_screen()
            elif self.state == "game":
                self.game_loop()
            elif self.state == "leaderboard":
                self.leaderboard_screen()
            elif self.state == "settings":
                self.settings_screen()
            elif self.state == "game_over":
                self.game_over_screen()