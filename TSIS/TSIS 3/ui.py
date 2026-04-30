import pygame

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (120, 120, 120)
DARK = (35, 35, 35)
BLUE = (45, 120, 255)
GREEN = (40, 180, 90)
RED = (220, 60, 60)
YELLOW = (245, 210, 60)


class Button:
    def __init__(self, x, y, w, h, text, color=BLUE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color

    def draw(self, screen, font):
        mouse = pygame.mouse.get_pos()
        color = tuple(min(255, c + 25) for c in self.color) if self.rect.collidepoint(mouse) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=12)
        text_img = font.render(self.text, True, WHITE)
        screen.blit(text_img, text_img.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_text(screen, text, x, y, font, color=WHITE, center=False):
    img = font.render(str(text), True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)


def draw_panel(screen, rect):
    pygame.draw.rect(screen, (30, 30, 30), rect, border_radius=18)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=18)
