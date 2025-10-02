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
        
        self.pos = None         # current position on screen (x, y)
        self.target_pos = None  # destination
        self.speed = 10         # pixels per tick or can use duration
        self.moving = False   
    
    def move_to(self, target_pos, speed=10):
        self.target_pos = target_pos
        self.speed = speed
        self.moving = True
        
    
    def update_position(self):
        if not self.moving or self.pos is None or self.target_pos is None:
            return

        x, y = self.pos
        tx, ty = self.target_pos

        # Compute direction
        dx = tx - x
        dy = ty - y
        distance = (dx**2 + dy**2) ** 0.5

        if distance <= self.speed:
            # Arrived
            self.pos = self.target_pos
            self.moving = False
        else:
            # Move proportionally
            x += dx / distance * self.speed
            y += dy / distance * self.speed
            self.pos = (x, y)
        
    def __repr__(self):
        return f"|{self.color}|"