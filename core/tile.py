import random

class Tile:
    def __init__(self, color):
        """
        Represents a single tile.
        color: int
        """
        self.color = color
        self.rotation = 0
        if color != -1:
            self.rotation = random.uniform(-30, 30)
            
        self.middle_pos = None
        
        self.pos = None          # current screen position
        self.last_render_pos = None  # last drawn position
    
    def __repr__(self):
        return f"|{self.color}|"