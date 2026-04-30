import pygame
import os
from racer import WIDTH, HEIGHT, FPS, RacerGame, CAR_COLORS, load_player_skins, PLAYER_SKIN_FILES
from ui import Button, draw_text, draw_panel, WHITE, BLUE, GREEN, RED, YELLOW
from persistence import load_settings, save_settings, load_leaderboard, add_score

pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    pass

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3 Racer")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)
big_font = pygame.font.SysFont("Arial", 50, bold=True)

settings = load_settings()
username = "Player"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(BASE_DIR, "assets", "sounds")
current_music = None


def play_music(filename):
    global current_music
    if not settings.get("sound", True):
        pygame.mixer.music.stop()
        current_music = None
        return
    if current_music == filename:
        return
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(SOUNDS_DIR, filename))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
        current_music = filename
    except Exception:
        current_music = None


def stop_music():
    global current_music
    pygame.mixer.music.stop()
    current_music = None


def input_username():
    global username
    text = ""
    while True:
        screen.fill((25, 25, 35))
        draw_text(screen, "Enter your name", WIDTH // 2, 190, big_font, WHITE, True)
        pygame.draw.rect(screen, WHITE, (100, 320, 300, 55), 2, border_radius=8)
        draw_text(screen, text or "Player", 115, 335, font, WHITE)
        draw_text(screen, "Press ENTER to start", WIDTH // 2, 425, small_font, YELLOW, True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    username = text.strip() or "Player"
                    return
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif len(text) < 12 and event.unicode.isprintable():
                    text += event.unicode
        pygame.display.flip()
        clock.tick(FPS)


def main_menu():
    play_music("menu.mp3")
    buttons = [
        Button(150, 230, 200, 50, "Play", GREEN),
        Button(150, 300, 200, 50, "Garage", YELLOW),
        Button(150, 370, 200, 50, "Leaderboard", BLUE),
        Button(150, 440, 200, 50, "Settings", YELLOW),
        Button(150, 510, 200, 50, "Quit", RED),
    ]
    while True:
        screen.fill((18, 18, 28))
        draw_text(screen, "RACER", WIDTH // 2, 120, big_font, WHITE, True)
        for b in buttons:
            b.draw(screen, font)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if buttons[0].clicked(event):
                input_username()
                return "play"
            if buttons[1].clicked(event):
                return "garage"
            if buttons[2].clicked(event):
                return "leaderboard"
            if buttons[3].clicked(event):
                return "settings"
            if buttons[4].clicked(event):
                return "quit"
        pygame.display.flip()
        clock.tick(FPS)


def garage_screen():
    global settings
    play_music("menu.mp3")
    skins = load_player_skins()
    left = Button(85, 520, 95, 45, "< Left", BLUE)
    right = Button(320, 520, 95, 45, "Right >", BLUE)
    save_back = Button(160, 620, 180, 50, "Save / Back", GREEN)
    while True:
        index = int(settings.get("car_skin", 0)) % len(skins)
        screen.fill((22, 22, 34))
        draw_text(screen, "GARAGE", WIDTH // 2, 110, big_font, WHITE, True)
        draw_text(screen, "Change skin with buttons or keyboard arrows", WIDTH // 2, 170, small_font, WHITE, True)
        draw_panel(screen, pygame.Rect(175, 240, 150, 220))
        preview = pygame.transform.scale(skins[index], (70, 125))
        screen.blit(preview, preview.get_rect(center=(WIDTH // 2, 345)))
        draw_text(screen, f"Skin {index + 1}: {PLAYER_SKIN_FILES[index]}", WIDTH // 2, 480, font, YELLOW, True)
        left.draw(screen, font)
        right.draw(screen, font)
        save_back.draw(screen, font)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if left.clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT):
                settings["car_skin"] = (index - 1) % len(skins)
                save_settings(settings)
            if right.clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
                settings["car_skin"] = (index + 1) % len(skins)
                save_settings(settings)
            if save_back.clicked(event) or (event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_RETURN]):
                save_settings(settings)
                return "menu"
        pygame.display.flip()
        clock.tick(FPS)


def leaderboard_screen():
    play_music("menu.mp3")
    back = Button(170, 710, 160, 45, "Back", BLUE)
    while True:
        screen.fill((20, 20, 30))
        draw_text(screen, "TOP 10", WIDTH // 2, 70, big_font, WHITE, True)
        scores = load_leaderboard()
        y = 140
        if not scores:
            draw_text(screen, "No scores yet", WIDTH // 2, 360, font, WHITE, True)
        for i, item in enumerate(scores, 1):
            line = f"{i}. {item['name']}  Score:{item['score']}  {item['distance']}m"
            draw_text(screen, line, 55, y, small_font, WHITE)
            y += 38
        back.draw(screen, font)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if back.clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return "menu"
        pygame.display.flip()
        clock.tick(FPS)


def settings_screen():
    global settings
    play_music("menu.mp3")
    colors = list(CAR_COLORS.keys())
    difficulties = ["easy", "normal", "hard"]
    buttons = [
        Button(120, 210, 260, 45, "Toggle Sound", BLUE),
        Button(120, 300, 260, 45, "Car Color", GREEN),
        Button(120, 390, 260, 45, "Difficulty", YELLOW),
        Button(170, 650, 160, 45, "Back", RED),
    ]
    while True:
        screen.fill((22, 22, 34))
        draw_text(screen, "SETTINGS", WIDTH // 2, 90, big_font, WHITE, True)
        draw_text(screen, f"Sound: {'ON' if settings['sound'] else 'OFF'}", 145, 170, font, WHITE)
        draw_text(screen, f"Car color: {settings['car_color']}", 145, 260, font, WHITE)
        draw_text(screen, f"Difficulty: {settings['difficulty']}", 145, 350, font, WHITE)
        draw_text(screen, "For car image skin use GARAGE", WIDTH // 2, 500, small_font, YELLOW, True)
        for b in buttons:
            b.draw(screen, font)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if buttons[0].clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)
                play_music("menu.mp3") if settings["sound"] else stop_music()
            if buttons[1].clicked(event):
                i = (colors.index(settings["car_color"]) + 1) % len(colors)
                settings["car_color"] = colors[i]
                save_settings(settings)
            if buttons[2].clicked(event):
                i = (difficulties.index(settings["difficulty"]) + 1) % len(difficulties)
                settings["difficulty"] = difficulties[i]
                save_settings(settings)
            if buttons[3].clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return "menu"
        pygame.display.flip()
        clock.tick(FPS)


def game_over_screen(result):
    play_music("menu.mp3")
    add_score(result["name"], result["score"], result["distance"], result["coins"])
    retry = Button(115, 560, 120, 45, "Retry", GREEN)
    menu = Button(265, 560, 120, 45, "Menu", BLUE)
    while True:
        screen.fill((25, 25, 35))
        title = "FINISHED!" if result.get("finished") else "GAME OVER"
        draw_text(screen, title, WIDTH // 2, 135, big_font, WHITE, True)
        draw_panel(screen, pygame.Rect(85, 240, 330, 210))
        draw_text(screen, f"Score: {result['score']}", 130, 285, font, WHITE)
        draw_text(screen, f"Distance: {result['distance']} m", 130, 335, font, WHITE)
        draw_text(screen, f"Coins: {result['coins']}", 130, 385, font, WHITE)
        retry.draw(screen, font)
        menu.draw(screen, font)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if retry.clicked(event):
                return "play"
            if menu.clicked(event):
                return "menu"
        pygame.display.flip()
        clock.tick(FPS)


def main():
    state = "menu"
    last_result = None
    while True:
        if state == "menu":
            state = main_menu()
        elif state == "garage":
            state = garage_screen()
        elif state == "settings":
            state = settings_screen()
        elif state == "leaderboard":
            state = leaderboard_screen()
        elif state == "play":
            play_music("background.mp3")
            game = RacerGame(screen, clock, settings, username)
            state, last_result = game.run()
        elif state == "game_over":
            state = game_over_screen(last_result)
        elif state == "quit":
            pygame.quit()
            break


if __name__ == "__main__":
    main()
