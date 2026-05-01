import os
import random
import math
import pygame

# -------------------- BASIC GAME SETTINGS --------------------
WIDTH, HEIGHT = 500, 800
FPS = 80
ROAD_LEFT = 120
ROAD_RIGHT = 380
LANES = [ROAD_LEFT + 40, (ROAD_LEFT + ROAD_RIGHT) // 2, ROAD_RIGHT - 40]
FINISH_DISTANCE = 3000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images")
SOUND_DIR = os.path.join(BASE_DIR, "assets", "sounds")

PLAYER_SKIN_FILES = ["main_car.jpg", "NPC1.jpg", "NPC2.jpg", "NPC3.jpg", "NPC4.jpg", "NPC5.jpg"]
NPC_FILES = ["NPC1.jpg", "NPC2.jpg", "NPC3.jpg"]

CAR_COLORS = {
    "blue": (60, 140, 255),
    "red": (230, 60, 60),
    "green": (40, 190, 90),
    "yellow": (240, 210, 60),
}

DIFFICULTY = {
    "easy": {"enemy": 5, "spawn": 90, "road": 4, "event": 1000},
    "normal": {"enemy": 6, "spawn": 75, "road": 5, "event": 850},
    "hard": {"enemy": 7, "spawn": 60, "road": 6, "event": 700},
}


def load_image(name, size, fallback_color):
    """Load an image from assets/images. If it is missing, draw a colored fallback."""
    path = os.path.join(IMAGE_DIR, name)
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except Exception:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(surf, fallback_color, surf.get_rect(), border_radius=8)
        pygame.draw.rect(surf, (255, 255, 255), surf.get_rect(), 2, border_radius=8)
        return surf


def load_sound(name):
    try:
        return pygame.mixer.Sound(os.path.join(SOUND_DIR, name))
    except Exception:
        return None


def load_player_skins():
    return [load_image(name, (40, 70), (70, 140, 255)) for name in PLAYER_SKIN_FILES]


def tint_surface(surface, color):
    """Add a light color overlay so the Settings car color is visible even with jpg skins."""
    result = surface.copy()
    overlay = pygame.Surface(result.get_size(), pygame.SRCALPHA)
    overlay.fill((*color, 45))
    result.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    return result


class Player(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        skins = load_player_skins()
        skin_index = int(settings.get("car_skin", 0)) % len(skins)
        self.color = CAR_COLORS.get(settings.get("car_color", "blue"), CAR_COLORS["blue"])
        self.image = tint_surface(skins[skin_index], self.color)
        self.rect = self.image.get_rect(center=(LANES[1], HEIGHT - 100))
        self.speed = 6
        self.shield = False
        self.crashes = 0

    def update(self, keys):
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > ROAD_LEFT:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < ROAD_RIGHT:
            self.rect.x += self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 0:
            self.rect.y -= self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        self.rect.clamp_ip(pygame.Rect(ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, self.color, self.rect.inflate(6, 6), 2, border_radius=8)
        if self.shield:
            pygame.draw.ellipse(screen, (80, 180, 255), self.rect.inflate(18, 18), 3)


class FallingObject(pygame.sprite.Sprite):
    def __init__(self, kind, x, y, speed, image, value=0, vx=0, moving=False):
        super().__init__()
        self.kind = kind
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.value = value
        self.vx = vx
        self.moving = moving
        self.start_x = x
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speed
        if self.moving:
            age = (pygame.time.get_ticks() - self.spawn_time) / 1000
            self.rect.centerx = int(self.start_x + math.sin(age * 4) * 45)
            self.rect.clamp_ip(pygame.Rect(ROAD_LEFT, -100, ROAD_RIGHT - ROAD_LEFT, HEIGHT + 200))
        else:
            self.rect.x += self.vx
        if self.rect.top > HEIGHT + 50:
            self.kill()


def create_coin(speed):
    choice = random.choices(
        [("1coin.jpg", 1), ("3coin.jpg", 3), ("5coin.jpg", 5)],
        weights=[75, 20, 5],
    )[0]
    img = load_image(choice[0], (25, 25), (245, 210, 40))
    return FallingObject("coin", random.choice(LANES), -40, speed, img, choice[1])


def safe_lane(forbidden_x=None):
    """Choose a lane that is not directly above the player."""
    if forbidden_x is None:
        return random.choice(LANES)
    safe = [x for x in LANES if abs(x - forbidden_x) > 60]
    return random.choice(safe) if safe else random.choice(LANES)


def create_enemy(speed, forbidden_x=None):
    img = load_image(random.choice(NPC_FILES), (40, 70), (190, 40, 40))
    return FallingObject("enemy", safe_lane(forbidden_x), -90, speed, img)


def make_obstacle_image(kind, wide=False):
    w, h = (82, 34) if wide else (54, 34)
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    if kind == "oil":
        pygame.draw.ellipse(surf, (20, 20, 20), (0, 3, w, 28))
        pygame.draw.ellipse(surf, (80, 80, 80), (10, 8, 20, 10))
    elif kind == "bump":
        pygame.draw.rect(surf, (255, 190, 40), (0, 8, w, 18), border_radius=6)
        pygame.draw.line(surf, (0, 0, 0), (5, 17), (w - 5, 17), 3)
    else:
        pygame.draw.rect(surf, (230, 80, 60), (0, 0, w, h), border_radius=6)
        pygame.draw.rect(surf, (255, 255, 255), (5, 8, w - 10, 6))
    return surf


def create_obstacle(speed, forbidden_x=None):
    kind = random.choice(["oil", "bump", "barrier"])
    return FallingObject(kind, safe_lane(forbidden_x), -40, speed, make_obstacle_image(kind))


def create_moving_barrier(speed, forbidden_x=None):
    return FallingObject(
        "barrier",
        safe_lane(forbidden_x),
        -50,
        speed,
        make_obstacle_image("barrier", wide=True),
        moving=True,
    )


def create_powerup(speed):
    kind = random.choice(["nitro", "shield", "repair"])
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    colors = {"nitro": (70, 170, 255), "shield": (80, 220, 140), "repair": (255, 90, 90)}
    pygame.draw.circle(surf, colors[kind], (20, 20), 18)
    pygame.draw.circle(surf, (255, 255, 255), (20, 20), 18, 2)
    font = pygame.font.SysFont("Arial", 22, bold=True)
    letter = {"nitro": "N", "shield": "S", "repair": "+"}[kind]
    txt = font.render(letter, True, (255, 255, 255))
    surf.blit(txt, txt.get_rect(center=(20, 20)))
    return FallingObject(kind, random.choice(LANES), -40, speed, surf)


def create_nitro_strip(speed):
    surf = pygame.Surface((70, 35), pygame.SRCALPHA)
    pygame.draw.rect(surf, (50, 170, 255), (0, 0, 70, 35), border_radius=8)
    pygame.draw.polygon(surf, (255, 255, 255), [(12, 8), (28, 17), (12, 27)])
    pygame.draw.polygon(surf, (255, 255, 255), [(35, 8), (51, 17), (35, 27)])
    return FallingObject("nitro_strip", random.choice(LANES), -50, speed, surf)


class RacerGame:
    def __init__(self, screen, clock, settings, username):
        self.screen = screen
        self.clock = clock
        self.settings = settings
        self.username = username
        self.road = load_image("Road.jpg", (WIDTH, HEIGHT), (60, 60, 60))
        self.player = Player(settings)
        self.objects = pygame.sprite.Group()
        self.font = pygame.font.SysFont("Arial", 22)
        self.small_font = pygame.font.SysFont("Arial", 17)
        self.big_font = pygame.font.SysFont("Arial", 44, bold=True)
        self.distance = 0
        self.coins = 0
        self.score = 0
        self.road_y1 = 0
        self.road_y2 = -HEIGHT
        self.finished = False
        self.game_over = False
        self.active_power = None
        self.power_end = 0
        self.road_event_text = ""
        self.road_event_end = 0
        self.coin_sound = load_sound("coin.mp3")
        self.crash_sound = load_sound("crash.mp3")
        diff = settings.get("difficulty", "easy")
        config = DIFFICULTY.get(diff, DIFFICULTY["easy"])
        self.base_enemy_speed = config["enemy"]
        self.spawn_delay = config["spawn"]
        self.road_scroll = config["road"]
        self.event_delay = config["event"]
        self.frame = 0

    def play_sound(self, snd):
        if self.settings.get("sound", True) and snd:
            snd.play()

    def draw_road(self):
        speed = self.road_scroll + self.distance // 900
        if self.active_power == "nitro":
            speed += 2
        self.road_y1 += speed
        self.road_y2 += speed
        if self.road_y1 >= HEIGHT:
            self.road_y1 = -HEIGHT
        if self.road_y2 >= HEIGHT:
            self.road_y2 = -HEIGHT
        self.screen.blit(self.road, (0, int(self.road_y1)))
        self.screen.blit(self.road, (0, int(self.road_y2)))

    def current_speed(self):
        speed = self.base_enemy_speed + self.distance // 550
        if self.active_power == "nitro":
            speed += 3
        return speed

    def start_road_event(self):
        """Dynamic road events: moving barrier wave, speed bumps, or nitro strip."""
        speed = self.current_speed()
        event = random.choice(["moving_barriers", "speed_bumps", "nitro_strip", "lane_hazard"])
        self.road_event_end = pygame.time.get_ticks() + 1800

        if event == "moving_barriers":
            self.road_event_text = "ROAD EVENT: MOVING BARRIER"
            self.objects.add(create_moving_barrier(speed + 1, self.player.rect.centerx))
        elif event == "speed_bumps":
            self.road_event_text = "ROAD EVENT: SPEED BUMPS"
            safe = safe_lane(self.player.rect.centerx)
            for lane in LANES:
                if lane != safe:
                    self.objects.add(FallingObject("bump", lane, -50 - random.randint(0, 120), speed, make_obstacle_image("bump")))
        elif event == "nitro_strip":
            self.road_event_text = "ROAD EVENT: NITRO STRIP"
            self.objects.add(create_nitro_strip(speed))
        else:
            self.road_event_text = "ROAD EVENT: SAFE PATH"
            safe = safe_lane(self.player.rect.centerx)
            for lane in LANES:
                if lane != safe:
                    self.objects.add(FallingObject("oil", lane, -50 - random.randint(0, 120), speed, make_obstacle_image("oil")))

    def spawn_logic(self):
        self.frame += 1
        progress = self.distance // 400
        delay = max(22, self.spawn_delay - progress * 3)
        speed = self.current_speed()

        # Dynamic traffic and obstacle density increases with progress.
        if self.frame % delay == 0:
            self.objects.add(create_enemy(speed, self.player.rect.centerx))
        if self.frame % max(35, delay + 18) == 0:
            self.objects.add(create_obstacle(speed, self.player.rect.centerx))
        if self.frame % 75 == 0:
            self.objects.add(create_coin(speed))
        if self.frame % 380 == 0:
            self.objects.add(create_powerup(speed))
        if self.frame % max(260, self.event_delay - int(progress) * 18) == 0:
            self.start_road_event()

    def activate_power(self, kind):
        # Only one active power-up at a time. Repair is instant, so it is allowed anytime.
        if kind == "repair":
            for obj in list(self.objects):
                if obj.kind in ["oil", "bump", "barrier"]:
                    obj.kill()
                    break
            self.score += 50
            self.road_event_text = "REPAIR USED: OBSTACLE CLEARED"
            self.road_event_end = pygame.time.get_ticks() + 1600
            return

        if self.active_power is not None:
            return

        self.active_power = kind
        if kind == "nitro":
            self.power_end = pygame.time.get_ticks() + 4000
        elif kind == "shield":
            self.player.shield = True
            self.power_end = 0

    def handle_collision(self, obj):
        if obj.kind == "coin":
            self.coins += obj.value
            self.score += obj.value * 10
            self.play_sound(self.coin_sound)
            obj.kill()
        elif obj.kind in ["nitro", "shield", "repair"]:
            self.activate_power(obj.kind)
            obj.kill()
        elif obj.kind == "nitro_strip":
            if self.active_power is None:
                self.activate_power("nitro")
            self.score += 20
            obj.kill()
        elif obj.kind in ["enemy", "barrier"]:
            if self.player.shield:
                self.player.shield = False
                self.active_power = None
                self.score += 25
                obj.kill()
            else:
                self.play_sound(self.crash_sound)
                self.game_over = True
        elif obj.kind == "oil":
            self.player.rect.x += random.choice([-35, 35])
            self.player.rect.clamp_ip(pygame.Rect(ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))
            self.score = max(0, self.score - 10)
            obj.kill()
        elif obj.kind == "bump":
            self.distance = max(0, self.distance - 25)
            self.score = max(0, self.score - 5)
            obj.kill()

    def update_power_time(self):
        if self.active_power == "nitro" and pygame.time.get_ticks() > self.power_end:
            self.active_power = None
        for obj in list(self.objects):
            if obj.kind in ["nitro", "shield", "repair"] and pygame.time.get_ticks() - obj.spawn_time > 6000:
                obj.kill()

    def draw_hud(self):
        remaining = max(0, FINISH_DISTANCE - self.distance)
        lines = [
            f"Name: {self.username}",
            f"Score: {int(self.score)}",
            f"Coins: {self.coins}",
            f"Distance: {int(self.distance)} m",
            f"Remaining: {int(remaining)} m",
        ]
        y = 8
        for line in lines:
            img = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(img, (8, y))
            y += 24

        if self.active_power:
            if self.active_power == "nitro":
                left = max(0, (self.power_end - pygame.time.get_ticks()) // 1000 + 1)
                text = f"Power: NITRO {left}s"
            elif self.active_power == "shield":
                text = "Power: SHIELD until hit"
            else:
                text = f"Power: {self.active_power.upper()}"
            img = self.small_font.render(text, True, (255, 240, 80))
            self.screen.blit(img, (WIDTH - img.get_width() - 10, 8))

        if self.road_event_text and pygame.time.get_ticks() < self.road_event_end:
            panel = pygame.Rect(95, 138, 310, 34)
            pygame.draw.rect(self.screen, (20, 20, 20), panel, border_radius=10)
            pygame.draw.rect(self.screen, (255, 240, 80), panel, 2, border_radius=10)
            img = self.small_font.render(self.road_event_text, True, (255, 240, 80))
            self.screen.blit(img, img.get_rect(center=panel.center))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit", self.result()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu", self.result()

            keys = pygame.key.get_pressed()
            self.player.update(keys)
            self.spawn_logic()
            self.objects.update()
            self.update_power_time()

            for obj in pygame.sprite.spritecollide(self.player, self.objects, False):
                self.handle_collision(obj)

            self.distance += 0.08 * self.current_speed()
            self.score += 0.03 * self.current_speed()
            if self.distance >= FINISH_DISTANCE:
                self.finished = True
                self.score += 500
                self.game_over = True

            self.draw_road()
            self.objects.draw(self.screen)
            self.player.draw(self.screen)
            self.draw_hud()

            pygame.display.flip()
            self.clock.tick(FPS)

            if self.game_over:
                pygame.time.delay(500)
                return "game_over", self.result()

    def result(self):
        return {
            "name": self.username,
            "score": int(self.score),
            "distance": int(self.distance),
            "coins": int(self.coins),
            "finished": self.finished,
        }