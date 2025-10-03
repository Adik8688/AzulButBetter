import pygame
from ui.utils import render_text_with_outline

class ButtonRenderer:
    def __init__(self, screen, size=(120, 50), margin = 20):
        self.screen = screen
        self.size = size
        self.margin = margin
        self.buttons = {}  # store button_id -> pygame.Rect

    def draw_undo_button(self, pos=None):
        screen_width, screen_height = self.screen.get_size()
        width, height = self.size
        
        x, y = self.margin, screen_height - height - self.margin
        if pos is not None:
            x, y = pos

        # Draw red arrow (triangle) pointing left
        arrow_points = [
            (x + 10, y + height // 2),    # tip
            (x + 40, y + 10),             # top back
            (x + 40, y + height - 10)     # bottom back
        ]
        
        pygame.draw.polygon(self.screen, (255, 0, 0), arrow_points)

        # Draw label using outline text
        font = pygame.font.SysFont(None, 32)
        text_surf = render_text_with_outline("UNDO", font, text_color=(255,255,255), outline_color=(0,0,0))
        text_rect = text_surf.get_rect(midleft=(x + 45, y + height // 2))
        self.screen.blit(text_surf, text_rect)

        # Store button rect
        self.buttons['undo'] = pygame.Rect(x, y, width, height)

        return self.buttons['undo']

    def get_button_rect(self, button_id):
        return self.buttons.get(button_id)
