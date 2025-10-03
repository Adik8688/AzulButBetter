# ui/renderer.py
from ui.board_renderer import PlayerBoardRenderer
from ui.factory_renderer import FactoryRenderer
from ui.assets_manager import AssetManager
from ui.button_renderer import ButtonRenderer
from ui.tile_renderer import TileRenderer

from core.game_logic import AzulGame

BAG_X_RATIO = 0.02
BAG_Y_RATIO = 0.05

TILES_SELECTED_X_RATIO = 0.15
TILES_SELECTED_Y_RATIO = 0.008

class Renderer:
    def __init__(self, screen, asset_manager: AssetManager, game_logic: AzulGame):
        self.screen = screen
        self.width, self.height = screen.get_size()
        
        self.assets = asset_manager
        self.game_logic = game_logic
        
        # assets loaded directly
        self.background = self.assets.load_image("background.jpg", scale=0.5)
        self.bag = self.assets.load_image("bag.png", scale=0.8)

        # renderers
        self.board_renderer = PlayerBoardRenderer(screen, asset_manager, board_scale=0.75)
        self.factory_renderer = FactoryRenderer(screen, asset_manager, self.game_logic.num_factories, factory_scale=0.8)
        self.tile_renderer = TileRenderer(screen, asset_manager)
        
        # undo
        self.button_renderer = ButtonRenderer(screen)
        
    
    def draw_background(self):
        bg_width, bg_heigth = self.background.get_size()
        
        for x in range(0, self.width, bg_width):
            for y in range(0, self.height, bg_heigth):
                self.screen.blit(self.background, (x, y))
    
    def draw_bag(self):
        X, Y = 50, 70
        self.screen.blit(self.bag, (X, Y))
    
    def draw_undo_button(self):
        self.button_renderer.draw_undo_button()
    
    def draw_selected_tiles(self):
        SPACING = 59
        X, Y = 450, 10
        
        for i, tile in enumerate(self.game_logic.selected_tiles):
            pos = (X + i * SPACING, Y)
            self.tile_renderer.draw_tile(tile, pos, rotate=False)
        
    def draw_factories(self):
        self.factory_renderer.draw_factories(self.game_logic.factories)
        self.factory_renderer.draw_middle(self.game_logic.middle)

    def draw_boards(self):
        board_rects = []
        for player in self.game_logic.players:
            
            if self.game_logic.is_selection():
                rect = self.board_renderer.draw_board(player, self.game_logic.current_player, self.game_logic.possible_moves())
            else:
                rect = self.board_renderer.draw_board(player, self.game_logic.current_player, None)
            
            board_rects.append(rect)

        return board_rects
    
    def draw(self):
        self.draw_background()
        self.draw_bag()
        self.draw_selected_tiles()
        
        if self.game_logic.selected_tiles:
            self.draw_undo_button()
        
        self.draw_factories()
        self.draw_boards()