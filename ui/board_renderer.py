# ui/board_renderer.py
import pygame
from core.player import Player


MARGIN = 20
SPACING = 50
NICKNAME_FONT_SIZE = 24

class PlayerBoardRenderer:
    def __init__(self, screen, asset_manager, board_scale=1):
        self.screen = screen
        self.assets = asset_manager
        
        self.board_img = self.assets.load_image("board.jpg", board_scale)


    def draw_player_name(self, name, color, x, y):
        """Draw player's name with shadow effect."""
        font = pygame.font.SysFont(None, NICKNAME_FONT_SIZE)
        shadow = font.render(name, True, color)
        text = font.render(name, True, (0, 0, 0))

        name_x = x + 90 - text.get_width() // 2
        name_y = y + 80 - text.get_height() - 5

        self.screen.blit(shadow, (name_x + 2, name_y + 2))
        self.screen.blit(text, (name_x, name_y))
    
    
    def draw_board(self, player: Player, current_player, possible_moves):
        """Draw board in 2-column layout anchored to right edge."""
        board_w, board_h = self.board_img.get_size()
        screen_width, _ = self.screen.get_size()

        # Determine column (0 = left col, 1 = right col)
        col, row = player.number % 2, player.number // 2

        # X: offset from right edge depending on column
        x = screen_width - (board_w + MARGIN) * (2 if col == 0 else 1)
        
        # Y: stacked per row
        y = MARGIN + row * (board_h + SPACING)

        # Outline rectangle
        outline_rect = pygame.Rect(x - 3, y - 3, board_w + 6, board_h + 6)
        pygame.draw.rect(self.screen, player.color, outline_rect, 3, border_radius=4)

        # Board image
        self.screen.blit(self.board_img, (x, y))

        # Player name (with shadow)
        self.draw_player_name(player.name, player.color, x, y)

        if possible_moves and player.number == current_player:
            self._highlight_valid_rows(possible_moves, x, y)
            

        return pygame.Rect(x, y, board_w, board_h)
    
    def _highlight_valid_rows(self, possible_moves: list, board_x, board_y):
        """
        Draw red dotted outlines around valid rows (0-4) and the floor row (-1).
        
        player: Player object (for accessing board if needed)
        possible_moves: list of dicts, each with "row", "to_row", "to_floor"
        board_x, board_y: top-left coordinates of the board image
        tile_size: height of one tile (square)
        spacing: spacing between tiles in a row
        """
        SIZE = 51
        SPACING = 8
        
        # filter to only moves that can actually place at least one tile in row
        valid_rows = [m["row"] for m in possible_moves if m["to_row"] > 0 or (m["row"] == -1 and m["to_floor"] > 0)]
        if not valid_rows:
            return

        x_right = board_x + 295
        
        # Draw pattern rows (0-4)
        for row_idx in range(5):
            if row_idx not in valid_rows:
                continue

            num_tiles = row_idx + 1
            row_width = SIZE * num_tiles + SPACING * (num_tiles - 1)
            row_height = SIZE
            rx = x_right - row_width
            ry = board_y + 10 + row_idx * (row_height + SPACING)

            rect = pygame.Rect(rx, ry, row_width, row_height)
            self.draw_dotted_rect(rect, color=(255, 0, 0), dot_size=4, gap=6, width=2)

        
        num_tiles = 7
        row_width = SIZE * num_tiles + SPACING * (num_tiles - 1) + 40
        row_height = SIZE * 1.2
        rx = x_right - row_width + 150
        # Position floor row just below the 5th pattern row
        ry = board_y + 5 * (row_height + SPACING) - 2

        rect = pygame.Rect(rx, ry, row_width, row_height)
        self.draw_dotted_rect(rect, color=(255, 0, 0), dot_size=4, gap=6, width=2)

    def draw_dotted_rect(self, rect, color=(255, 0, 0), dot_size=4, gap=4, width=2):
        """Draw a dotted rectangle around a given rect."""
        # Top & bottom
        for x in range(rect.left, rect.right, dot_size + gap):
            pygame.draw.line(self.screen, color, (x, rect.top), (min(x + dot_size, rect.right), rect.top), width)
            pygame.draw.line(self.screen, color, (x, rect.bottom), (min(x + dot_size, rect.right), rect.bottom), width)
        # Left & right
        for y in range(rect.top, rect.bottom, dot_size + gap):
            pygame.draw.line(self.screen, color, (rect.left, y), (rect.left, min(y + dot_size, rect.bottom)), width)
            pygame.draw.line(self.screen, color, (rect.right, y), (rect.right, min(y + dot_size, rect.bottom)), width)
