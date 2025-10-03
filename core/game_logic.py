# core/game_round.py
import random
from core.tile import Tile
from core.factory import Factory
from core.middle import Middle
from random import shuffle


class AzulGame:
    def __init__(self, players):
        
        self.players = players
        shuffle(self.players)
        self.current_player = 0
        
        self.num_factories = 1 + 2 * len(players)
        self.factories = [Factory() for _ in range(self.num_factories)]
        self.middle = Middle()
        self.bag = self._create_bag()
        self.discard = []
        
        self.selected_tiles = []
        self.last_selection_info = None
        
    def is_selection(self):
        return bool(self.selected_tiles)
    
    def get_selected_tiles(self):
        return sorted(self.selected_tiles)        

    def next_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)     
    
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
        self.middle.tile_first_taken = False

    def player_select_from_factory(self, factory_index, color):
        factory = self.factories[factory_index]
        chosen, remaining = factory.take_tiles(color)

        self.last_selection_info = {
            "origin": "factory",
            "factory_idx": factory_index,
            "selected_tiles": chosen,
            "remaining_to_middle": remaining,
            "middle_first_player_prev": self.middle.tile_first_taken
        }

        # Move remaining tiles to middle
        if remaining:
            self.middle.add_tiles(remaining)
            
        self.selected_tiles = chosen
        
        print(f"Color {color} taken from factory {factory_index}")
        print(f"Selected tiles: {self.selected_tiles}")
        
        moves = self.possible_moves()
        for m in moves:
            print(m)
            
        return chosen
    
    def player_select_from_middle(self, color):
        if self.selected_tiles:
            # Already have selected tiles — ignore until placed or undone
            return []
        
        chosen = self.middle.take_tiles(color)
        self.selected_tiles = chosen
        # store last selection info for undo
        self.last_selection_info = {
            "origin": "middle",
            "selected_tiles": chosen,
            "first_tile_taken": self.middle.tile_first_taken
        }
            
        print(f"Selected tiles: {self.selected_tiles}")
        
        moves = self.possible_moves()
        for m in moves:
            print(m)
            
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
            self.middle.tile_first_taken = info["middle_first_player_prev"]

        elif info["origin"] == "middle":
            # Return tiles to middle
            self.middle.add_tiles(info["selected_tiles"])
            if info["first_tile_taken"]:
                self.middle.tile_first_taken = not info["first_tile_taken"]

        # Clear selection
        self.selected_tiles = []
        self.last_selection_info = None
        
        print(f"Undo:")
        print(f"Info: {info}")
        
    def possible_moves(self):
        """
        Generate all possible moves for current player based on self.selected_tiles.
        Returns a list of dicts:
            {
                "row": row_idx (0–4 or -1 for floor),
                "to_row": number_of_tiles_placed_in_row,
                "to_floor": number_of_tiles_to_floor (includes -1 markers)
            }
        """
        if not self.selected_tiles:
            return []

        current_player = self.players[self.current_player]
        board = current_player.board

        # Separate normal tiles and markers
        normal_tiles = [t for t in self.selected_tiles if t.color != -1]
        markers = [t for t in self.selected_tiles if t.color == -1]
        count_normal = len(normal_tiles)
        count_marker = len(markers)

        moves = []

        if count_normal > 0:
            color = normal_tiles[0]  # all normal tiles are the same color
            # Check pattern rows
            for row_idx in range(board.SIZE):
                if board.can_place(row_idx, color):
                    free_slots = (row_idx + 1) - len(board.rows[row_idx])
                    to_row = min(count_normal, free_slots)
                    to_floor = count_normal - to_row + count_marker  # include marker
                    moves.append({
                        "row": row_idx,
                        "to_row": to_row,
                        "to_floor": to_floor
                    })

        # Floor line move: all tiles (normal + marker) go to floor
        moves.append({
            "row": -1,
            "to_row": 0,
            "to_floor": count_normal + count_marker
        })

        return moves


    