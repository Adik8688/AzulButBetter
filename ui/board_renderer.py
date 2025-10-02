# ui/board_renderer.py
import pygame
NICKNAME_MARGIN_RATIO_LEFT = 0.14
NICKNAME_MARGIN_RATIO_TOP = 0.19
NICKNAME_FONT_SIZE = 23

class PlayerBoardRenderer:
    def __init__(self, screen, asset_manager, board_scale=1, margin=20, spacing=20):
        self.screen = screen
        self.assets = asset_manager
        self.original_board_img = self.assets.load_image("board.jpg")
        self.scale = board_scale
        self.margin = margin
        self.spacing = spacing


    def draw_board(self, player, index):
        """Draw board in 2-column layout anchored to right edge."""
        w, h = self.original_board_img.get_size()
        board_w, board_h = int(w * self.scale), int(h * self.scale)
        board_img = pygame.transform.smoothscale(self.original_board_img, (board_w, board_h))

        screen_width, _ = self.screen.get_size()

        # Determine column (0 = left col, 1 = right col)
        col = index % 2
        row = index // 2

        # X: offset from right edge depending on column
        if col == 0:  # left column (P1, P3, etc.)
            x = screen_width - (board_w * 2 + self.margin * 3) + self.margin
        else:         # right column (P2, P4, etc.)
            x = screen_width - board_w - self.margin

        # Y: stacked per row
        y = self.margin + row * (board_h + self.spacing)

        # Outline rectangle
        outline_rect = pygame.Rect(x - 3, y - 3, board_w + 6, board_h + 6)
        pygame.draw.rect(self.screen, player.color, outline_rect, 3, border_radius=4)


        # Board image
        self.screen.blit(board_img, (x, y))

        # Player name (with shadow)
        font = pygame.font.SysFont(None, NICKNAME_FONT_SIZE)
        shadow = font.render(player.name, True, player.color)
        text = font.render(player.name, True, (0, 0, 0))
        name_x = x + board_w * NICKNAME_MARGIN_RATIO_LEFT - text.get_width() // 2
        name_y = y + board_h * NICKNAME_MARGIN_RATIO_TOP - text.get_height() - 5
        self.screen.blit(shadow, (name_x + 2, name_y + 2))
        self.screen.blit(text, (name_x, name_y))

        return pygame.Rect(x, y, board_w, board_h)