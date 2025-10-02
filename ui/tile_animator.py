# ui/tile_animator.py
import math

class TileAnimator:
    def __init__(self):
        self.active_tiles = []  # list of tiles being animated

    def add(self, tile, target_pos, speed=15):
        """
        Start moving a tile to a target position.
        tile: Tile instance
        target_pos: (x, y) tuple
        speed: pixels per tick
        """
        tile.target_pos = target_pos
        tile.speed = speed
        tile.moving = True
        if tile.pos is None:
            tile.pos = target_pos  # initialize if not set
        self.active_tiles.append(tile)

    def update(self):
        """
        Call every frame to move tiles.
        Removes tiles from active list once they reach destination.
        """
        finished = []
        for tile in self.active_tiles:
            if not tile.moving:
                finished.append(tile)
                continue

            x, y = tile.pos
            tx, ty = tile.target_pos
            dx = tx - x
            dy = ty - y
            distance = math.hypot(dx, dy)

            if distance <= tile.speed:
                tile.pos = tile.target_pos
                tile.moving = False
                finished.append(tile)
            else:
                x += dx / distance * tile.speed
                y += dy / distance * tile.speed
                tile.pos = (x, y)

        # remove finished tiles
        self.active_tiles = [t for t in self.active_tiles if t not in finished]

    def is_animating(self):
        """Returns True if any tile is still moving"""
        return len(self.active_tiles) > 0

    def clear(self):
        """Stop all animations"""
        for tile in self.active_tiles:
            tile.moving = False
            tile.pos = tile.target_pos
        self.active_tiles.clear()
