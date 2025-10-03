import random

class Tile:
    def __init__(self, color):
        self.color = color
        self.rotation = 0
        if color != -1:
            self.rotation = random.uniform(-30, 30)
            
        self.middle_pos = None
        
        self.pos = None 
    
    def __repr__(self):
        return f"|{self.color}|"