# ui/renderer.py
from ui.board_renderer import PlayerBoardRenderer
from ui.factory_renderer import FactoryRenderer
from ui.assets_manager import AssetManager
from ui.button_renderer import ButtonRenderer

from core.game_logic import FactoryGame

BAG_X_RATIO = 0.02
BAG_Y_RATIO = 0.05

TILES_SELECTED_X_RATIO = 0.15
TILES_SELECTED_Y_RATIO = 0.008

class Renderer:
    def __init__(self, screen, asset_manager: AssetManager, game_logic: FactoryGame):
        self.screen = screen
        self.assets = asset_manager
        self.game_logic = game_logic
        
        self.background = self.assets.load_image("background.jpg", scale=0.5)
        self.bg_width, self.bg_height = self.background.get_size()
        
        self.bag = self.assets.load_image("bag.png", scale=0.8)

        # Board renderer
        self.board_renderer = PlayerBoardRenderer(screen, asset_manager, board_scale=0.75, spacing=50)
        self.factory_renderer = FactoryRenderer(screen, asset_manager, self.game_logic.num_factories, factory_scale=0.8)
        
        # undo
        self.button_renderer = ButtonRenderer(screen)

        
    def draw_background(self):
        screen_width, screen_height = self.screen.get_size()
        for x in range(0, screen_width, self.bg_width):
            for y in range(0, screen_height, self.bg_height):
                self.screen.blit(self.background, (x, y))

        self.screen.blit(self.bag, (screen_width * BAG_X_RATIO, screen_height * BAG_Y_RATIO))

        # Draw undo button
        if self.game_logic.selected_tiles:
            self.button_renderer.draw_undo_button()
    
    def draw_selected_tiles(self, ):
        """
        Draw currently selected tiles stacked horizontally.
        :param start_pos: top-left position where first tile is drawn
        :param spacing: horizontal distance between tiles
        """
        spacing = 59
        screen_width, screen_height = self.screen.get_size()
        x, y = screen_width * TILES_SELECTED_X_RATIO, screen_height * TILES_SELECTED_Y_RATIO
        
        # 1 board 4th row
        #x, y = 967, 207
        
        for i, tile in enumerate(self.game_logic.selected_tiles):
            tile.rotation = 0  # reset rotation for selected tiles
            pos = (x + i * spacing, y)
            self.factory_renderer.tile_renderer.draw_tile(tile, pos)
        

    def draw_boards(self):
        """Draw all player boards with names and outlines."""
        board_rects = []
        for i, player in enumerate(self.game_logic.players):
            rect = self.board_renderer.draw_board(player, i)
            board_rects.append(rect)
        return board_rects
    
    def draw_factories(self):
        self.factory_renderer.draw_factories(self.game_logic.factories)
        self.factory_renderer.draw_middle(self.game_logic.middle)
