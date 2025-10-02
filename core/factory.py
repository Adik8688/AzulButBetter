# core/factory.py
class Factory:
    def __init__(self, capacity=4):
        self.capacity = capacity
        self.tiles = []

    def is_full(self):
        return len(self.tiles) >= self.capacity

    def add_tiles(self, tiles):
        space = self.capacity - len(self.tiles)
        self.tiles.extend(tiles[:space])

    def take_tiles(self, color: int):
        chosen = [t for t in self.tiles if t.color == color]
        remaining = [t for t in self.tiles if t.color != color]
        self.tiles = []
        return chosen, remaining
