import pygame
import math

# -----------------------------------
# Settings
# -----------------------------------
WIDTH, HEIGHT = 900, 650
TOOLBAR_HEIGHT = 100
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
    # Draw text on the screen
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def make_rect(x, y, w, h):
    # Create pygame rectangle object
    return pygame.Rect(x, y, w, h)


def normalize_rect(start_pos, end_pos):
    # Convert two points into a normal rectangle
    x1, y1 = start_pos
    x2, y2 = end_pos
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x1 - x2)
    height = abs(y1 - y2)
    return pygame.Rect(left, top, width, height)


def get_square_rect(start_pos, end_pos):
    # Build a square using the smaller side
    x1, y1 = start_pos
    x2, y2 = end_pos

    side = min(abs(x2 - x1), abs(y2 - y1))

    if x2 >= x1:
        left = x1
    else:
        left = x1 - side

    if y2 >= y1:
        top = y1
    else:
        top = y1 - side

    return pygame.Rect(left, top, side, side)


def get_right_triangle_points(start_pos, end_pos):
    # Right triangle with legs parallel to axes
    x1, y1 = start_pos
    x2, y2 = end_pos
    return [(x1, y1), (x1, y2), (x2, y2)]


def get_equilateral_triangle_points(start_pos, end_pos):
    # Build an equilateral triangle from dragged width
    x1, y1 = start_pos
    x2, y2 = end_pos

    side = abs(x2 - x1)

    # Avoid zero-size triangle
    if side == 0:
        side = 1

    height = (math.sqrt(3) / 2) * side

    # Direction depends on mouse movement
    if x2 >= x1:
        left_x = x1
        right_x = x1 + side
    else:
        left_x = x1 - side
        right_x = x1

    mid_x = (left_x + right_x) / 2

    # If dragging downward, apex goes downward; otherwise upward
    if y2 >= y1:
        apex_y = y1 + height
        base_y = y1
    else:
        apex_y = y1 - height
        base_y = y1

    return [
        (left_x, base_y),
        (right_x, base_y),
        (mid_x, apex_y)
    ]


def get_rhombus_points(start_pos, end_pos):
    # Rhombus inside the rectangle formed by two points
    x1, y1 = start_pos
    x2, y2 = end_pos

    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    left = min(x1, x2)
    right = max(x1, x2)
    top = min(y1, y2)
    bottom = max(y1, y2)

    return [
        (center_x, top),      # top point
        (right, center_y),    # right point
        (center_x, bottom),   # bottom point
        (left, center_y)      # left point
    ]


def draw_toolbar(screen, current_tool, current_color, brush_size, font):
    # Toolbar background
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 2)

    tools = [
        "brush", "rectangle", "circle",
        "square", "right_triangle", "equilateral_triangle",
        "rhombus", "eraser", "clear"
    ]

    tool_buttons = {}

    # Smaller buttons
    button_w = 110
    button_h = 24
    gap = 8

    x = 10
    y = 5

    label_map = {
        "brush": "Brush",
        "rectangle": "Rect",
        "circle": "Circle",
        "square": "Square",
        "right_triangle": "R-Tri",
        "equilateral_triangle": "E-Tri",
        "rhombus": "Rhombus",
        "eraser": "Eraser",
        "clear": "Clear"
    }

    for tool in tools:
        rect = pygame.Rect(x, y, button_w, button_h)
        tool_buttons[tool] = rect

        button_color = DARK_GRAY if current_tool == tool else WHITE
        text_color = WHITE if current_tool == tool else BLACK

        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        draw_text(screen, label_map[tool], rect.x + 8, rect.y + 4, font, text_color)

        x += button_w + gap

        # New row if no space
        if x + button_w > WIDTH:
            x = 10
            y += button_h + 5

    # Colors
    color_buttons = []
    x = 10
    y = 65

    for color in COLOR_OPTIONS:
        rect = pygame.Rect(x, y, 30, 20)
        color_buttons.append((rect, color))

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        x += 38

    draw_text(screen, f"Size: {brush_size}", 320, 67, font)
    draw_text(screen, "+ / - size", 430, 67, font)

    return tool_buttons, color_buttons


def draw_brush(surface, color, start, end, radius):
    # Draw a smooth line by placing many circles
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
    # Keep mouse position inside canvas area
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

    font = pygame.font.SysFont("Arial", 16)

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

        # Draw toolbar and get all buttons
        tool_buttons, color_buttons = draw_toolbar(
            screen, current_tool, current_color, brush_size, font
        )

        # Draw saved canvas
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
                elif event.key == pygame.K_s:
                    current_tool = "square"
                elif event.key == pygame.K_t:
                    current_tool = "right_triangle"
                elif event.key == pygame.K_q:
                    current_tool = "equilateral_triangle"
                elif event.key == pygame.K_h:
                    current_tool = "rhombus"
                elif event.key == pygame.K_e:
                    current_tool = "eraser"

                # Brush size hotkeys
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

                    # Convert screen coordinates to canvas coordinates
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

                # Free drawing only for brush and eraser
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

                # Draw selected shape on mouse release
                if current_tool == "rectangle":
                    rect = normalize_rect(canvas_start, canvas_end)
                    pygame.draw.rect(canvas, current_color, rect, 2)

                elif current_tool == "circle":
                    rect = normalize_rect(canvas_start, canvas_end)
                    pygame.draw.ellipse(canvas, current_color, rect, 2)

                elif current_tool == "square":
                    rect = get_square_rect(canvas_start, canvas_end)
                    pygame.draw.rect(canvas, current_color, rect, 2)

                elif current_tool == "right_triangle":
                    points = get_right_triangle_points(canvas_start, canvas_end)
                    pygame.draw.polygon(canvas, current_color, points, 2)

                elif current_tool == "equilateral_triangle":
                    points = get_equilateral_triangle_points(canvas_start, canvas_end)
                    pygame.draw.polygon(canvas, current_color, points, 2)

                elif current_tool == "rhombus":
                    points = get_rhombus_points(canvas_start, canvas_end)
                    pygame.draw.polygon(canvas, current_color, points, 2)

                drawing = False
                start_pos = None
                preview_pos = None
                last_pos = None

        # Draw preview while dragging
        if drawing and current_tool in (
            "rectangle", "circle", "square",
            "right_triangle", "equilateral_triangle", "rhombus"
        ) and start_pos and preview_pos:
            temp_surface = screen.copy()

            preview_start = start_pos
            preview_end = preview_pos

            # Convert preview coordinates to canvas coordinates
            canvas_preview_start = (
                preview_start[0],
                preview_start[1] - TOOLBAR_HEIGHT
            )
            canvas_preview_end = (
                preview_end[0],
                preview_end[1] - TOOLBAR_HEIGHT
            )

            # Draw preview directly on screen with toolbar offset
            if current_tool == "rectangle":
                rect = normalize_rect(preview_start, preview_end)
                pygame.draw.rect(temp_surface, current_color, rect, 2)

            elif current_tool == "circle":
                rect = normalize_rect(preview_start, preview_end)
                pygame.draw.ellipse(temp_surface, current_color, rect, 2)

            elif current_tool == "square":
                rect = get_square_rect(preview_start, preview_end)
                pygame.draw.rect(temp_surface, current_color, rect, 2)

            elif current_tool == "right_triangle":
                points = get_right_triangle_points(preview_start, preview_end)
                pygame.draw.polygon(temp_surface, current_color, points, 2)

            elif current_tool == "equilateral_triangle":
                points = get_equilateral_triangle_points(preview_start, preview_end)
                pygame.draw.polygon(temp_surface, current_color, points, 2)

            elif current_tool == "rhombus":
                points = get_rhombus_points(preview_start, preview_end)
                pygame.draw.polygon(temp_surface, current_color, points, 2)

            screen.blit(temp_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()