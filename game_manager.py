import pygame
import sys

from core.player import Player
from ui.renderer import Renderer
from ui.assets_manager import AssetManager

from core.game_logic import AzulGame

# Game settings
WIDTH, HEIGHT = 2200, 900
FPS = 60
DEBUG_MAX_PLAYERS = 3

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Azul (Prototype)")
        self.clock = pygame.time.Clock()
        self.running = True
        self.assets = AssetManager()
        
        self.last_click_time = 0
        self.click_delay = 150  

        # Players
        self.players = [
            Player("Oddajmake"),
            Player("Ni88achu"),
            Player("Dolphie-hottie"),
            Player("Twój Stary"),
        ]
        self.players = self.players[:DEBUG_MAX_PLAYERS]

        self.game_logic = AzulGame(self.players)
        self.renderer = Renderer(self.screen, self.assets, self.game_logic)
        

    def fill_factories(self):
        """Draw tiles from the bag to fill each factory"""
        for factory in self.factories:
            tiles_to_draw = min(factory.capacity, len(self.bag))
            drawn = [self.bag.pop() for _ in range(tiles_to_draw)]
            factory.add_tiles(drawn)


    def player_take_from_factory(self, factory_index, color):
        """
        Player picks tiles of a color from a factory
        - Returns tiles chosen by player
        - Moves remaining tiles to middle
        """
        factory = self.factories[factory_index]
        chosen, remaining = factory.take_tiles(color)
        if remaining:
            self.middle.add_tiles(remaining)
        return chosen
    
    def player_take_from_middle(self, color):
        """
        Player picks tiles from middle
        """
        return self.middle.take_tiles(color)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_click_time < self.click_delay:
                    # Ignore rapid clicks
                    continue
                self.last_click_time = current_time

                pos = event.pos
                undo_rect = self.renderer.button_renderer.get_button_rect('undo')
                if undo_rect and undo_rect.collidepoint(pos):
                    if self.game_logic.selected_tiles:
                        self.game_logic.undo_selection()
                        continue
                for rect, (origin, factory_idx, color) in self.renderer.factory_renderer.tile_click_map:
                    if rect.collidepoint(pos):
                        if origin == "factory":
                            chosen = self.game_logic.player_select_from_factory(factory_idx, color)
                            for t in chosen:
                                t.origin = "factory"
                                t.factory_idx = factory_idx
                        elif origin == "middle":
                            chosen = self.game_logic.player_select_from_middle(color)
                            for t in chosen:
                                t.origin = "middle"
                        continue


    def update(self, dt):
        """Update game state each frame."""
        
        # TODO: Add Azul-specific game logic here
        pass

    def draw(self):
        self.renderer.draw()
        
        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            if self.game_logic.is_empty():
                self.game_logic.fill_factories()
                
            
                
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            self.handle_events()
            self.update(dt)
            self.draw()

        self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameManager()
    game.run()
