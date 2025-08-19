import pygame
from config import COLOR_BLUE, COLOR_WHITE, COLOR_GRAY_DARK, COLOR_BLACK

class Button:
    def __init__(self, x, y, width, height, text, font, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.callback = callback
        self.color = COLOR_BLUE
        self.text_color = COLOR_WHITE
        self.is_hovered = False
        self.is_selected = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.callback:
                self.callback()

    def draw(self, screen, is_selected=False):
        color = tuple(min(c + 40, 255) for c in self.color) if is_selected else self.color
        color = tuple(min(c + 20, 255) for c in color) if self.is_hovered else color
        
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        if self.text:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

class Panel:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, COLOR_BLACK, self.rect, 2)

def draw_text(screen, text, font, color, center_pos):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=center_pos)
    screen.blit(text_surf, text_rect)