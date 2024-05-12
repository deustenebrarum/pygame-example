import math
import pygame

from utility.character import Direction
from utility.collision_box import CollisionBox


class Sword(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        self.image = pygame.image.load("./assets/characters/mHeroHand_.png")
        self.image = pygame.transform.scale(self.image, (15, 15))

        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        self.collision_box = CollisionBox(position, (15, 15))
        self.direction = Direction.RIGHT
        self._position = pygame.Vector2(position)

    @property
    def position(self):
        return self._position

    def set_position(self, position):
        self._position.x = position.x
        self._position.y = position.y

    def update(self):
        angle = (pygame.time.get_ticks() / 20) % 360
        self.rect.x = int(self._position[0] + math.cos(math.radians(angle)) * 100)
        self.rect.y = int(self._position[1] + math.sin(math.radians(angle)) * 100)

        self.collision_box.x = self.rect.x
        self.collision_box.y = self.rect.y

        super().update()