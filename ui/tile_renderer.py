import pygame
from ui.assets_manager import AssetManager

TILES_MAP = {
    -1: 'tile_first.png',
    1: 'tile_cyan.png',
    2: 'tile_red.png',
    3: 'tile_blue.png',
    4: 'tile_yellow.png',
    5: 'tile_black.png'
}

class TileRenderer:
    def __init__(self, screen, asset_manager: AssetManager, tile_size=50):
        self.screen = screen
        self.assets = asset_manager
        self.tile_size = tile_size
        self.tile_images = {}  # cache for scaled images
    
    def _get_tile_image(self, tile):
        """Get scaled image for tile color (cached)."""
        if tile.color not in self.tile_images:
            if tile.color not in TILES_MAP:
                raise ValueError(f"No asset defined for tile color {tile.color}")
            asset_name = TILES_MAP[tile.color]
            img = self.assets.load_image(asset_name, scale=0.4)
            self.tile_images[tile.color] = pygame.transform.smoothscale(
                img, (self.tile_size, self.tile_size)
            )
        return self.tile_images[tile.color]
    
    
    def _make_tile_with_outline(self, img, outline_color=(0, 0, 0), thickness=2):
        # create a slightly larger surface with alpha
        size = (img.get_width() + thickness*2, img.get_height() + thickness*2)
        outlined = pygame.Surface(size, pygame.SRCALPHA)

        # draw outline (rect or circle depending on your style)
        rect = outlined.get_rect()
        pygame.draw.rect(outlined, outline_color, rect, border_radius=6)

        # blit the tile centered
        outlined.blit(img, (thickness, thickness))
        return outlined
    
    def draw_tile(self, tile, pos, rotate=True, shadow=True, outline=True):
        # Initialize animation properties
        if not hasattr(tile, "screen_pos"):
            tile.screen_pos = pos
            tile.target_pos = pos
            tile.start_pos = pos
            tile.progress = 1
            tile.animating = False

        # If renderer suggests new target
        if pos != tile.target_pos:
            tile.start_pos = tile.screen_pos
            tile.target_pos = pos
            tile.progress = 0
            tile.animating = True

        # Animate if needed
        if tile.animating:
            speed = 0.08
            tile.progress += speed
            if tile.progress >= 1:
                tile.progress = 1
                tile.animating = False

            # Interpolate
            x = tile.start_pos[0] + (tile.target_pos[0] - tile.start_pos[0]) * tile.progress
            y = tile.start_pos[1] + (tile.target_pos[1] - tile.start_pos[1]) * tile.progress
            tile.screen_pos = (x, y)
        else:
            tile.screen_pos = tile.target_pos

        # --- Drawing at animated screen_pos ---
        img = self._get_tile_image(tile)
        outlined = self._make_tile_with_outline(img, outline_color=(0, 0, 0))

        if rotate:
            outlined = pygame.transform.rotate(outlined, tile.rotation)

        rect = outlined.get_rect(center=(tile.screen_pos[0] + self.tile_size // 2,
                                        tile.screen_pos[1] + self.tile_size // 2))

        # shadow pass
        if shadow:
            shadow_img = outlined.copy()
            shadow_img.fill((0, 0, 0, 120), special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.blit(shadow_img, (rect.x + 4, rect.y + 4))

        self.screen.blit(outlined, rect.topleft)

        return rect

