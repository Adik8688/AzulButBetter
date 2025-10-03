# core/factory.py
class Factory:
    def __init__(self, capacity=4):
        self.capacity = capacity
        self.tiles = []

    def add_tiles(self, tiles):
        self.tiles.extend(tiles)
        if len(tiles) > self.capacity:
            raise Exception(f'Over {self.capacity} tiles on the plate')

    def take_tiles(self, color: int):
        chosen = [t for t in self.tiles if t.color == color]
        remaining = [t for t in self.tiles if t.color != color]
        self.tiles = []
        return chosen, remaining
