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
    def __init__(self, screen, asset_manager: AssetManager, tile_size=120):
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
        
        draw_pos = tile.pos if tile.pos is not None else pos
        if draw_pos is None:
            raise ValueError("Tile has no position to draw at")
        
        img = self._get_tile_image(tile)
        outlined = self._make_tile_with_outline(img, outline_color=(0,0,0))

        if rotate:
            outlined = pygame.transform.rotate(outlined, tile.rotation)

        rect = outlined.get_rect(center=(pos[0] + self.tile_size // 2,
                                        pos[1] + self.tile_size // 2))

        # shadow pass
        if shadow:
            shadow_img = outlined.copy()
            shadow_img.fill((0,0,0,120), special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.blit(shadow_img, (rect.x+4, rect.y+4))

        # final tile
        self.screen.blit(outlined, rect.topleft)
        
        return rect
