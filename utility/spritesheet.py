import pygame


class SpriteSheet:
    def __init__(self, filename, scale):
        self.spritesheet = pygame.image.load(filename).convert()
        self.scale = scale

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return pygame.transform.scale(image, (image.get_width() * self.scale, image.get_height() * self.scale))
