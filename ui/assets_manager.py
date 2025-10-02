import pygame
import os

class AssetManager:
    def __init__(self, asset_dir="ui/assets"):
        """
        scale: global scaling factor for assets (e.g., 0.5 = half size)
        asset_dir: folder where images are stored
        """
        self.asset_dir = asset_dir
        self.cache = {}

    def load_image(self, filename, scale=1.0):
        """Load and scale an image, caching it for reuse."""
        if filename in self.cache:
            return self.cache[filename]

        path = os.path.join(self.asset_dir, filename)
        image = pygame.image.load(path).convert_alpha()

        if scale != 1.0:
            w, h = image.get_size()
            image = pygame.transform.smoothscale(
                image, (int(w * scale), int(h * scale))
            )

        self.cache[filename] = image
        return image
