class Middle:
    def __init__(self):
        self.tiles = []
        self.first_player_taken = False 

    def add_tiles(self, tiles: list):
        """Add regular tiles to the middle."""
        self.tiles.extend(tiles)

    def take_tiles(self, color: int):
        """
        Take all tiles of a given color from middle.
        If Tile(-1) is still present, it's automatically taken by the first player who draws from middle.
        """
        # Collect tiles of the chosen color
        chosen_tiles = [t for t in self.tiles if t.color == color]

        # Remove chosen tiles from middle
        self.tiles = [t for t in self.tiles if t.color != color]

        # Handle first-player tile
        if not self.first_player_taken and any(t.color == -1 for t in self.tiles):
            # Take Tile(-1) as well
            fp_tile_index = next(i for i, t in enumerate(self.tiles) if t.color == -1)
            chosen_tiles.append(self.tiles.pop(fp_tile_index))
            self.first_player_taken = True

        return chosen_tiles