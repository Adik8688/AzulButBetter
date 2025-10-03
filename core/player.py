# core/player.py

from core.board import Board

COLORS = [
    (0, 128, 255),  # Blue
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (255, 0, 255)   # Magenta
]

class Player:
    players_count = 0
    
    def __init__(self, name):
        self.name = name
        self.number = Player.players_count
        self.color = COLORS[(Player.players_count) % len(COLORS)]
        Player.increase_player_count()
        
        self.board = Board()

    @classmethod
    def increase_player_count(cls):
        cls.players_count += 1