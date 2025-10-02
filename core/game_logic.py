# core/game_round.py
import random
from core.tile import Tile
from core.factory import Factory
from core.middle import Middle


class FactoryGame:
    def __init__(self, players):
        
        self.players = players
        self.num_factories = 1 + 2 * len(players)
        self.factories = [Factory() for _ in range(self.num_factories)]
        self.middle = Middle()
        self.bag = self._create_bag()
        self.discard = []
        
        self.selected_tiles = []
        self.last_selection_info = None
        
        
    def is_empty(self):
        return not (any([f.tiles for f in self.factories]) or self.middle.tiles)
        
    def _create_bag(self):
        colors = [1, 2, 3, 4, 5]  # integers as tile colors
        bag = [Tile(c) for c in colors for _ in range(20)]
        random.shuffle(bag)
        return bag

    def fill_factories(self):
        for factory in self.factories:
            draw = min(factory.capacity, len(self.bag))
            tiles = [self.bag.pop() for _ in range(draw)]
            factory.add_tiles(tiles)
        
        self.middle.add_tiles([Tile(-1), Tile(1), Tile(1), Tile(1), ])
        self.middle.first_player_taken = False

    def player_take_from_factory(self, factory_index, color):
        factory = self.factories[factory_index]
        chosen, remaining = factory.take_tiles(color)

        self.last_selection_info = {
            "origin": "factory",
            "factory_idx": factory_index,
            "selected_tiles": chosen,
            "remaining_to_middle": remaining,
            "middle_first_player_prev": self.middle.first_player_taken
        }

        # Move remaining tiles to middle
        if remaining:
            self.middle.add_tiles(remaining)
            
        self.selected_tiles = chosen
        
        print(f"Color {color} taken from factory {factory_index}")
        print(f"Selected tiles: {self.selected_tiles}")
        return chosen
    
    def player_take_from_middle(self, color):
        if self.selected_tiles:
            # Already have selected tiles — ignore until placed or undone
            return []
        
        chosen = self.middle.take_tiles(color)
        self.selected_tiles = chosen
        # store last selection info for undo
        self.last_selection_info = {
            "origin": "middle",
            "selected_tiles": chosen,
            "first_tile_taken": self.middle.first_player_taken
        }
            
        print(f"Selected tiles: {self.selected_tiles}")
        
        return chosen
    
    def undo_selection(self):
        """Return selected tiles and leftovers back to origin, fully restoring previous state."""    
        if not self.last_selection_info:
            return

        info = self.last_selection_info

        if info["origin"] == "factory":
            factory_idx = info["factory_idx"]
            # Return selected tiles
            self.factories[factory_idx].add_tiles(info["selected_tiles"])
            # Return leftover tiles that went to middle
            if info["remaining_to_middle"]:
                # Remove from middle
                for t in info["remaining_to_middle"]:
                    if t in self.middle.tiles:
                        self.middle.tiles.remove(t)
                self.factories[factory_idx].add_tiles(info["remaining_to_middle"])
            # Restore first player tile state if needed
            self.middle.first_player_taken = info["middle_first_player_prev"]

        elif info["origin"] == "middle":
            # Return tiles to middle
            self.middle.add_tiles(info["selected_tiles"])
            if info["first_tile_taken"]:
                self.middle.first_player_taken = not info["first_tile_taken"]

        # Clear selection
        self.selected_tiles = []
        self.last_selection_info = None
        
        print(f"Undo:")
        print(f"Info: {info}")
        
        
    def print_debug(self):
        self.factories