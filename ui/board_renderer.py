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
    
    
    def draw_board(self, player: Player, selected_tiles):
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

        return pygame.Rect(x, y, board_w, board_h)
    
    def highlight_valid_rows(self, board, selected_tiles, x, start_y, end_y, tile_size=40, spacing=5, floor_y=None, floor_width=None):
        """
        Draw red dotted outlines for rows where at least 1 tile can be placed.
        - start_y / end_y: vertical bounds for the 5 pattern rows
        - tile_size: height of tiles (squared)
        - spacing: space between rows
        - floor_y: y position for floor line
        - floor_width: width of floor line
        """
        if not selected_tiles:
            return

        # Separate normal tiles from markers
        normal_tiles = [t for t in selected_tiles if t != -1]
        if not normal_tiles:
            return  # only marker → floor

        color = normal_tiles[0]

        # Determine valid rows
        moves = []
        for row_idx in range(board.SIZE):
            if board.can_place(row_idx, color):
                moves.append(row_idx)
        if not moves:
            return

        # Calculate vertical positions
        total_height = end_y - start_y
        row_height = tile_size  # row height = tile height
        # total required height = 5*tile_size + 4*spacing
        top_y = start_y

        for row_idx in moves:
            # Row width grows from 1 tile → 5 tiles
            row_width = tile_size * (row_idx + 1)
            # Right-aligned: board right edge is x + board_w
            x_right = x + board.board_width if hasattr(board, "board_width") else x + 200  # fallback width
            rx = x_right - row_width
            ry = top_y + row_idx * (row_height + spacing)
            rect = pygame.Rect(rx, ry, row_width, row_height)

            self.draw_dotted_rect(rect, color=(255, 0, 0), dot_size=4, gap=6, width=2)

        # Optionally draw floor line
        if floor_y is not None and floor_width is not None:
            rect = pygame.Rect(x + board.board_width - floor_width, floor_y, floor_width, tile_size)
            self.draw_dotted_rect(rect, color=(255, 0, 0), dot_size=4, gap=6, width=2)



    def draw_dotted_rect(self, rect, color=(255, 0, 0), dot_size=4, gap=4, width=2):
        """Draw a dotted rectangle around a given rect."""
        # horizontal lines
        for x in range(rect.left, rect.right, dot_size + gap):
            pygame.draw.line(self.screen, color, (x, rect.top), (min(x + dot_size, rect.right), rect.top), width)
            pygame.draw.line(self.screen, color, (x, rect.bottom), (min(x + dot_size, rect.right), rect.bottom), width)
        # vertical lines
        for y in range(rect.top, rect.bottom, dot_size + gap):
            pygame.draw.line(self.screen, color, (rect.left, y), (rect.left, min(y + dot_size, rect.bottom)), width)
            pygame.draw.line(self.screen, color, (rect.right, y), (rect.right, min(y + dot_size, rect.bottom)), width)