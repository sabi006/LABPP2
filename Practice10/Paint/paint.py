import pygame

# -----------------------------------
# Settings
# -----------------------------------
WIDTH, HEIGHT = 900, 650
TOOLBAR_HEIGHT = 90
CANVAS_Y = TOOLBAR_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (80, 80, 80)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)
ORANGE = (255, 140, 0)

COLOR_OPTIONS = [
    BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE
]


# -----------------------------------
# Helper functions
# -----------------------------------
def draw_text(screen, text, x, y, font, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def make_rect(x, y, w, h):
    return pygame.Rect(x, y, w, h)


def normalize_rect(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x1 - x2)
    height = abs(y1 - y2)
    return pygame.Rect(left, top, width, height)


def draw_toolbar(screen, current_tool, current_color, brush_size, font):
    # Toolbar background
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 2)

    # Tool buttons
    tools = ["brush", "rectangle", "circle", "eraser", "clear"]
    tool_buttons = {}

    x = 10
    for tool in tools:
        rect = make_rect(x, 10, 110, 30)
        tool_buttons[tool] = rect

        button_color = DARK_GRAY if current_tool == tool else WHITE
        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        text_color = WHITE if current_tool == tool else BLACK
        draw_text(screen, tool.capitalize(), rect.x + 10, rect.y + 5, font, text_color)
        x += 120

    # Color buttons
    color_buttons = []
    x = 10
    y = 50
    for color in COLOR_OPTIONS:
        rect = make_rect(x, y, 35, 25)
        color_buttons.append((rect, color))
        pygame.draw.rect(screen, color, rect)
        border_width = 4 if color == current_color else 2
        pygame.draw.rect(screen, BLACK, rect, border_width)
        x += 45

    # Info text
    draw_text(screen, f"Size: {brush_size}", 360, 52, font)
    draw_text(screen, "Keys: B-brush  R-rectangle  C-circle  E-eraser", 480, 10, font)
    draw_text(screen, "+ / - to change size", 480, 35, font)

    return tool_buttons, color_buttons


def draw_brush(surface, color, start, end, radius):
    # Smooth line with circles between points
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    steps = max(abs(dx), abs(dy))

    if steps == 0:
        pygame.draw.circle(surface, color, start, radius)
        return

    for i in range(steps + 1):
        x = int(start[0] + dx * i / steps)
        y = int(start[1] + dy * i / steps)
        pygame.draw.circle(surface, color, (x, y), radius)


def clamp_to_canvas(pos):
    x, y = pos
    x = max(0, min(WIDTH - 1, x))
    y = max(CANVAS_Y, min(HEIGHT - 1, y))
    return x, y


# -----------------------------------
# Main program
# -----------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Extended Paint Program")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 20)

    # Separate canvas surface
    canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(WHITE)

    current_tool = "brush"
    current_color = BLACK
    brush_size = 5

    drawing = False
    start_pos = None
    last_pos = None
    preview_pos = None

    running = True
    while running:
        screen.fill(WHITE)

        # Draw toolbar and get button rectangles
        tool_buttons, color_buttons = draw_toolbar(
            screen, current_tool, current_color, brush_size, font
        )

        # Draw canvas
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                # Tool hotkeys
                elif event.key == pygame.K_b:
                    current_tool = "brush"
                elif event.key == pygame.K_r:
                    current_tool = "rectangle"
                elif event.key == pygame.K_c:
                    current_tool = "circle"
                elif event.key == pygame.K_e:
                    current_tool = "eraser"

                # Brush size
                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                    brush_size = min(50, brush_size + 1)
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    brush_size = max(1, brush_size - 1)

                # Color hotkeys
                elif event.key == pygame.K_1:
                    current_color = BLACK
                elif event.key == pygame.K_2:
                    current_color = RED
                elif event.key == pygame.K_3:
                    current_color = GREEN
                elif event.key == pygame.K_4:
                    current_color = BLUE

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # Click on toolbar
                if my < TOOLBAR_HEIGHT:
                    for tool, rect in tool_buttons.items():
                        if rect.collidepoint(event.pos):
                            if tool == "clear":
                                canvas.fill(WHITE)
                            else:
                                current_tool = tool

                    for rect, color in color_buttons:
                        if rect.collidepoint(event.pos):
                            current_color = color

                # Click on canvas
                else:
                    drawing = True
                    start_pos = clamp_to_canvas(event.pos)
                    preview_pos = start_pos
                    last_pos = start_pos

                    # Convert to canvas coordinates
                    canvas_pos = (start_pos[0], start_pos[1] - TOOLBAR_HEIGHT)

                    if current_tool == "brush":
                        pygame.draw.circle(canvas, current_color, canvas_pos, brush_size)
                    elif current_tool == "eraser":
                        pygame.draw.circle(canvas, WHITE, canvas_pos, brush_size)

            elif event.type == pygame.MOUSEMOTION and drawing:
                preview_pos = clamp_to_canvas(event.pos)

                current_pos = clamp_to_canvas(event.pos)
                canvas_last = (last_pos[0], last_pos[1] - TOOLBAR_HEIGHT)
                canvas_current = (current_pos[0], current_pos[1] - TOOLBAR_HEIGHT)

                if current_tool == "brush":
                    draw_brush(canvas, current_color, canvas_last, canvas_current, brush_size)
                    last_pos = current_pos

                elif current_tool == "eraser":
                    draw_brush(canvas, WHITE, canvas_last, canvas_current, brush_size)
                    last_pos = current_pos

            elif event.type == pygame.MOUSEBUTTONUP and drawing:
                end_pos = clamp_to_canvas(event.pos)

                canvas_start = (start_pos[0], start_pos[1] - TOOLBAR_HEIGHT)
                canvas_end = (end_pos[0], end_pos[1] - TOOLBAR_HEIGHT)

                if current_tool == "rectangle":
                    rect = normalize_rect(canvas_start, canvas_end)
                    pygame.draw.rect(canvas, current_color, rect, 2)

                elif current_tool == "circle":
                    rect = normalize_rect(canvas_start, canvas_end)
                    pygame.draw.ellipse(canvas, current_color, rect, 2)

                drawing = False
                start_pos = None
                preview_pos = None
                last_pos = None

        # Draw preview for rectangle/circle while dragging
        if drawing and current_tool in ("rectangle", "circle") and start_pos and preview_pos:
            temp_surface = screen.copy()

            preview_start = start_pos
            preview_end = preview_pos

            rect = normalize_rect(
                (preview_start[0], preview_start[1]),
                (preview_end[0], preview_end[1])
            )

            if current_tool == "rectangle":
                pygame.draw.rect(temp_surface, current_color, rect, 2)
            elif current_tool == "circle":
                pygame.draw.ellipse(temp_surface, current_color, rect, 2)

            screen.blit(temp_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()