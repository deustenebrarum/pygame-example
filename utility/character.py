import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = pygame.Vector2(position)

        self.image = pygame.Surface(self.rect.size)
        self.image.fill((255, 255, 255))

    def update(self):
        pass