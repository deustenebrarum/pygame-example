import random
from enemies.enemy import Enemy
from enemy_spritesheets import GoblinSpriteSheet
from utility.character import (
    CharacterAnimationMachine, CharacterDirection, CharacterState
)


class GoblinAnimationMachine(CharacterAnimationMachine):
    def __init__(self):
        sprite_sheet = GoblinSpriteSheet()

        unit_px = 24

        super().__init__(
            sprite_sheet, (CharacterState.IDLE, CharacterDirection.LEFT),
            {
                (CharacterState.IDLE, CharacterDirection.RIGHT): (
                    0, 0
                ),
                (CharacterState.IDLE, CharacterDirection.LEFT): (
                    unit_px * 4 + 1, 0
                ),
                (CharacterState.WALKING, CharacterDirection.RIGHT): (
                    0, unit_px + 1
                ),
                (CharacterState.WALKING, CharacterDirection.LEFT): (
                    unit_px * 4 + 1, unit_px + 1
                ),
                (CharacterState.DYING, CharacterDirection.RIGHT): (
                    0, unit_px * 5 + 1
                ),
                (CharacterState.DYING, CharacterDirection.LEFT): (
                    unit_px * 4 + 1, unit_px * 5 + 1
                ),
            }
        )


class Goblin(Enemy):
    def __init__(self, position, clock, player):
        animation_machine = GoblinAnimationMachine()

        super().__init__(
            position, clock, player,
            animation_machine,
            collision_size=(44, 60),
            speed=int(Enemy.BASE_SPEED * 0.8),
            life_limit=random.randint(4000, 6000),
        )
