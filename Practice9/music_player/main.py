import pygame
from player import MusicPlayer

WIDTH, HEIGHT = 520, 280

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GRAY   = (200, 200, 200)
GREEN  = (50,  180,  80)
RED    = (200,  50,  50)
BLUE   = (50,  120, 220)
BG     = (30,   30,  45)
PANEL  = (50,   50,  70)


def draw(screen, player, font_big, font_med, font_small):
    screen.fill(BG)

    title = font_big.render("Music Player", True, WHITE)
    screen.blit(title, (20, 20))

    if player.is_playing:
        status_text  = "▶ Playing"
        status_color = GREEN
    else:
        status_text  = "⏹ Stopped"
        status_color = RED

    status = font_med.render(status_text, True, status_color)
    screen.blit(status, (20, 70))

    pygame.draw.rect(screen, PANEL, (20, 110, WIDTH - 40, 60), border_radius=8)

    track_label = font_small.render("Now playing:", True, GRAY)
    screen.blit(track_label, (35, 120))

    track_name = font_small.render(player.current_track_name(), True, WHITE)
    screen.blit(track_name, (35, 140))

    # ---------------- PROGRESS ----------------
    if player.is_playing:
        ms = pygame.mixer.music.get_pos()
        if ms < 0:
            ms = 0

        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60

        time_text = font_small.render(
            f"{minutes:02}:{seconds:02}",
            True,
            WHITE
        )
        screen.blit(time_text, (WIDTH - 70, 70))

        bar_x = 20
        bar_y = 200
        bar_w = WIDTH - 40
        bar_h = 8

        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_w, bar_h), border_radius=4)

        progress = (seconds % 30) / 30
        pygame.draw.rect(
            screen,
            BLUE,
            (bar_x, bar_y, bar_w * progress, bar_h),
            border_radius=4
        )

    # -----------------------------------------

    if player.playlist:
        num = font_small.render(
            f"Track {player.current_index + 1} of {len(player.playlist)}",
            True, GRAY
        )
        screen.blit(num, (20, 185))

    controls = font_small.render(
        "[P] Play   [S] Stop   [N] Next   [B] Back   [Q] Quit",
        True, GRAY
    )
    screen.blit(controls, (20, 240))


def main():
    pygame.init()
    pygame.key.set_repeat(0)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")

    font_big   = pygame.font.SysFont("Arial", 28, bold=True)
    font_med   = pygame.font.SysFont("Arial", 22)
    font_small = pygame.font.SysFont("Arial", 16)

    player = MusicPlayer()
    clock  = pygame.time.Clock()

    SONG_END = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(SONG_END)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.previous_track()
                elif event.key == pygame.K_q:
                    running = False

            if event.type == SONG_END:
                if not player.manual_change:
                    player.next_track()
                player.manual_change = False

        draw(screen, player, font_big, font_med, font_small)
        pygame.display.flip()
        clock.tick(30)

    player.stop()
    pygame.quit()


if __name__ == "__main__":
    main()