from enemies.enemy import Enemy
from enemy_spritesheets import GoblinSpriteSheet
from utility.character import CharacterDirection, CharacterState


class Skeleton(Enemy):
    def __init__(self, position, clock, player):
        super().__init__(
            position, clock, player, GoblinSpriteSheet,
            (11, 16), (13, 0),
            {
                (CharacterState.IDLE, CharacterDirection.RIGHT): (6, 8),
                (CharacterState.IDLE, CharacterDirection.LEFT): (103, 8),
                (CharacterState.WALKING, CharacterDirection.RIGHT): (6, 32),
                (CharacterState.WALKING, CharacterDirection.LEFT): (103, 32),
                (CharacterState.DYING, CharacterDirection.RIGHT): (6, 152),
                (CharacterState.DYING, CharacterDirection.LEFT): (103, 152),
            }
        )