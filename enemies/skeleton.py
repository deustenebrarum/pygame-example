import random
from enemies.enemy import Enemy
from enemy_spritesheets import SkeletonSpriteSheet
from utility.character import (
    CharacterAnimationMachine, CharacterDirection, CharacterState
)


class SkeletonAnimationMachine(CharacterAnimationMachine):
    def __init__(self):
        sprite_sheet = SkeletonSpriteSheet()

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
                    0, unit_px * 2 + 1
                ),
                (CharacterState.WALKING, CharacterDirection.LEFT): (
                    unit_px * 4 + 1, unit_px * 2 + 1
                ),
                (CharacterState.DYING, CharacterDirection.RIGHT): (
                    0, unit_px * 6 + 1
                ),
                (CharacterState.DYING, CharacterDirection.LEFT): (
                    unit_px * 4 + 1, unit_px * 6 + 1
                ),
            }
        )


class Skeleton(Enemy):
    def __init__(self, position, clock, player):
        animation_machine = SkeletonAnimationMachine()

        super().__init__(
            position, clock, player,
            animation_machine,
            collision_size=(44, 60),
            life_limit=random.randint(2000, 4000),
        )
