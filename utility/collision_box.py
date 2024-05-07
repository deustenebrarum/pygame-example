from typing import Sequence
import pygame


class CollisionBox(pygame.Rect):
    def __init__(self, position, size):
        super().__init__(*position, *size)

    def collides_with(self, other: pygame.Rect) -> bool:
        return self.colliderect(other)

    def get_group_collisions(
        self, others: Sequence[pygame.Rect]
    ) -> list[pygame.Rect]:
        return [other for other in others if self.collides_with(other)]

    def collides_any(self, others: Sequence[pygame.Rect]) -> bool:
        return len(self.get_group_collisions(others)) > 0
