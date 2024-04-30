import pygame

from utility.animation_machine import AnimationMachine


class Character(pygame.sprite.Sprite):
    def __init__(
        self, position,
        clock: pygame.time.Clock,
        animation_machine: AnimationMachine
    ):
        super().__init__()
        self.position = pygame.Vector2(position)
        self.animation_machine = animation_machine

        self.image = self.animation_machine.image
        self.rect = self.image.get_rect()

        self.clock = clock

    def update(self):
        self.rect.y = int(self.position.y)
        self.rect.x = int(self.position.x)

        self.animation_machine.update()
        self.image = self.animation_machine.image

    def select_animation(self, key):
        self.animation_machine.select(key)
