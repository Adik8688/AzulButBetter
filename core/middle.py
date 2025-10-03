# core/middle.py
class Middle:
    def __init__(self):
        self.tiles = []
        self.tile_first_taken = False 

    def add_tiles(self, tiles: list):
        self.tiles.extend(tiles)
        self.tiles = sorted(self.tiles, key= lambda x: x.color)

    def take_tiles(self, color: int):
        chosen_tiles = [t for t in self.tiles if t.color == color]
        self.tiles = [t for t in self.tiles if t.color != color]

        if not self.tile_first_taken:
            tile_first, self.tiles = self.tiles[0], self.tiles[1:]
            
            chosen_tiles.append(tile_first)
            self.tile_first_taken = True

        return chosen_tiles