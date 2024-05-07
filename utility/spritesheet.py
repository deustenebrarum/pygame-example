import pygame

from utility import constants


class SpriteSheet:
    SCALE = constants.PIXELS_PER_UNIT

    def __init__(self, filename, scale=1):
        self.spritesheet = pygame.image.load(filename)
        self.spritesheet = self.spritesheet.convert_alpha()
        self.scale = scale * self.SCALE

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(
            image,
            (
                image.get_width() * self.scale,
                image.get_height() * self.scale
            )
        )
        return image
