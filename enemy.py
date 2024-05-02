import pygame
from utility.character import Character, CharacterDirection, CharacterState

from enemy_spritesheets import get_random_sprite_sheet


class Enemy(Character):
    SPEED = 100
    LIFE_LIMIT = 1000 * 4

    def __init__(self, position, clock, player):
        sprite_sheet = get_random_sprite_sheet()

        super().__init__(
            position, clock, sprite_sheet,
            (11, 16), (13, 0),
            positionsByStates={
                (CharacterState.IDLE, CharacterDirection.RIGHT): (6, 8),
                (CharacterState.IDLE, CharacterDirection.LEFT): (103, 8),
                (CharacterState.WALKING, CharacterDirection.RIGHT): (6, 32),
                (CharacterState.WALKING, CharacterDirection.LEFT): (103, 32),
                (CharacterState.DYING, CharacterDirection.RIGHT): (6, 152),
                (CharacterState.DYING, CharacterDirection.LEFT): (103, 152),
            }
        )

        self.player = player

        self.speed = self.SPEED
        self.spawn_time = pygame.time.get_ticks()
        self.state = CharacterState.WALKING

    def update(self):
        if self.is_alive:
            self.move_to_player(self.player)

        if pygame.time.get_ticks() - self.spawn_time > self.LIFE_LIMIT:
            self.state = CharacterState.DYING

        super().update()

        if (
            (not self.is_alive) and
            self.animation_machine.animation.ended_once
        ):
            self.kill()

    def move_to_player(self, player):
        dt = self.clock.get_time() / 1000
        speed = self.speed * dt

        vector = (
            pygame.Vector2(player.position) -
            pygame.Vector2(self.position)
        )
        if vector.x < 0:
            self.direction = CharacterDirection.LEFT
        else:
            self.direction = CharacterDirection.RIGHT
        self.position += vector.normalize() * speed
