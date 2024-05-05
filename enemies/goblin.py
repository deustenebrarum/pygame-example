from enemies.enemy import Enemy
from enemy_spritesheets import GoblinSpriteSheet
from utility.character import CharacterAnimationMachine, CharacterDirection, CharacterState


class GoblinAnimationMachine(CharacterAnimationMachine):
    SIZE = (11, 16)
    DYING_SIZE = (15, 16)
    FRAME_SHIFT = (13, 0)

    def __init__(self):
        sprite_sheet = GoblinSpriteSheet()

        super().__init__(
            sprite_sheet, (CharacterState.IDLE, CharacterDirection.LEFT),
            {
                (CharacterState.IDLE, CharacterDirection.LEFT): (103, 9),
                (CharacterState.IDLE, CharacterDirection.RIGHT): (8, 9),
                (CharacterState.WALKING, CharacterDirection.LEFT): (103, 33),
                (CharacterState.WALKING, CharacterDirection.RIGHT): (8, 33),
                (CharacterState.DYING, CharacterDirection.RIGHT): (6, 128),
                (CharacterState.DYING, CharacterDirection.LEFT): (103, 128),
            },
            self.SIZE, self.FRAME_SHIFT
        )
        
        dyingRight = self.animations[(CharacterState.DYING, CharacterDirection.RIGHT)]
        dyingRight.change_params(
            size=self.DYING_SIZE,
            frame_shift=(9, 0)
        )

class Goblin(Enemy):
    def __init__(self, position, clock, player):
        animation_machine = GoblinAnimationMachine()
        
        super().__init__(
            position, clock, player,
            animation_machine
        )
