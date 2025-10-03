import pygame
import os

class AssetManager:
    def __init__(self, asset_dir="ui/assets"):
        self.asset_dir = asset_dir
        self.cache = {}

    def scale_img(self, img, scale):
        w, h = img.get_size()
        return pygame.transform.smoothscale(
                img, (int(w * scale), int(h * scale))
            )

    def load_image(self, filename, scale=1.0):
        if filename in self.cache:
            return self.cache[filename]

        path = os.path.join(self.asset_dir, filename)
        image = pygame.image.load(path).convert_alpha()

        if scale != 1.0:
            image = self.scale_img(image, scale)

        self.cache[filename] = image
        return image