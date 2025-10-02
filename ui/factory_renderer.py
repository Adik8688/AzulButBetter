# ui/factory_renderer.py
import pygame
import math
import random

from ui.assets_manager import AssetManager
from ui.tile_renderer import TileRenderer
from ui.utils import render_text_with_outline

CENTER_X_RATIO = 0.2
CENTER_Y_RATIO = 0.5
RADIUS_RATIO = 0.26

COLOR_OFFSETS = [
    (120, 0),      # right
    (0, -120),     # top
    (-120, 0),     # left
    (0, 120),      # bottom
    (85, -85),     # top-right diagonal
]

class FactoryRenderer:
    def __init__(self, screen, asset_manager: AssetManager, num_factories, factory_scale=1, tile_size=50):
        self.screen = screen
        self.assets = asset_manager
        self.num_factories = num_factories

        screen_width, screen_height = self.screen.get_size()
        self.center = (screen_width * CENTER_X_RATIO, screen_height * CENTER_Y_RATIO)
        self.radius = (screen_height + (num_factories - 5) * 100) * RADIUS_RATIO
        self.scale = factory_scale

        # Load factory plate image
        self.original_factory_img = self.assets.load_image("factory.png")
        w, h = self.original_factory_img.get_size()
        self.factory_w = int(w * self.scale)
        self.factory_h = int(h * self.scale)
        self.factory_img = pygame.transform.smoothscale(
            self.original_factory_img, (self.factory_w, self.factory_h)
        )

        # Tile renderer
        self.tile_renderer = TileRenderer(screen, asset_manager, tile_size=tile_size)
        self.tile_click_map = []
        
        self._group_angles = self._get_group_angles()
        
        
    def _get_group_angles(self):
        group_angles = {}
        
        offset = random.randint(1, 10)
        for i in range(1, 6):
            randomizer = (i + offset) % 5 + 1
            group_angles[i] = randomizer * (2 * math.pi / 5)

        return group_angles
            

    def draw_factories(self, factories):
        factories_info = []
        cx, cy = self.center
        self.tile_click_map = []  # reset click map each frame

        for i, factory in enumerate(factories):
            # arranging plates 
            
            angle = i * (2 * math.pi / self.num_factories) - math.pi / 2
            fx = cx + int(math.cos(angle) * self.radius) - self.factory_w // 2
            fy = cy + int(math.sin(angle) * self.radius) - self.factory_h // 2

            rect = pygame.Rect(fx, fy, self.factory_w, self.factory_h)
            self.screen.blit(self.factory_img, (fx, fy))

            # slots for tiles
            slot_radius = min(self.factory_w, self.factory_h) // 6
            slot_offsets = [
                (-slot_radius, -slot_radius),
                ( slot_radius, -slot_radius),
                (-slot_radius,  slot_radius),
                ( slot_radius,  slot_radius),
            ]

            slots = []
            
            # placing tiles in slots
            for j, tile in enumerate(factory.tiles):
                if j >= len(slot_offsets):
                    break
                ox, oy = slot_offsets[j]
                sx = fx + self.factory_w // 2 + ox
                sy = fy + self.factory_h // 2 + oy

                pos = (sx - self.tile_renderer.tile_size // 2,
                    sy - self.tile_renderer.tile_size // 2)
                rect_tile = self.tile_renderer.draw_tile(tile, pos)

                slots.append((sx, sy))
                self.tile_click_map.append((rect_tile, ("factory", i, tile.color)))

            factories_info.append((rect, slots))
            

        return factories_info


    def draw_middle(self, middle, radius=120):
        mx, my = self.center

        # Split tiles
        first_tile = None
        other_tiles = []
        for tile in middle.tiles:
            if tile.color == -1:
                first_tile = tile
            else:
                other_tiles.append(tile)

        # Draw the first player tile at the exact center
        if first_tile:
            if first_tile.middle_pos is None:
                first_tile.middle_pos = (mx - self.tile_renderer.tile_size // 2,
                                        my - self.tile_renderer.tile_size // 2)
            self.tile_renderer.draw_tile(first_tile, first_tile.middle_pos, rotate=True)

        if not other_tiles:
            return

        # Group tiles by color
        color_groups = {}
        for tile in other_tiles:
            color_groups.setdefault(tile.color, []).append(tile)


        font = pygame.font.SysFont(None, 40)

        # Draw each color group
        for color, tiles in color_groups.items():
            angle = self._group_angles[color]
            # Center position for this color group
            gx = mx + int(radius * math.cos(angle))
            gy = my + int(radius * math.sin(angle))

            # Draw tiles in stack with slight jitter
            for tile in tiles:
                if tile.middle_pos is None:
                    jitter_x = random.randint(-30, 30)
                    jitter_y = random.randint(-30, 30)
                    tile.middle_pos = (gx + jitter_x - self.tile_renderer.tile_size // 2,
                                    gy + jitter_y - self.tile_renderer.tile_size // 2)
                rect_tile = self.tile_renderer.draw_tile(tile, tile.middle_pos, rotate=True)
                self.tile_click_map.append((rect_tile, ("middle", None, tile.color)))

            # Draw count next to stack
            count_surf = render_text_with_outline(str(len(tiles)), font)
            text_pos = (gx + radius * 0.1, gy - 10)
            self.screen.blit(count_surf, text_pos)
