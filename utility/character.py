from enum import Enum
import pygame

from utility.animation import Animation
from utility.animation_machine import AnimationMachine


class CharacterState(Enum):
    IDLE = 0
    WALKING = 1
    DYING = 2


class CharacterDirection(Enum):
    LEFT = 0
    RIGHT = 1


class CharacterAnimationMachine(AnimationMachine):
    FPS = 8
    DYING_FPS = 2

    def __init__(
        self, sprite_sheet, current,
        positionsByStates, size, frame_shift=(13, 0)
    ):
        self.frame_shift = frame_shift
        self.size = size
        super().__init__(
            {
                (CharacterState.IDLE, CharacterDirection.LEFT): Animation(
                    sprite_sheet,
                    columns=4,
                    position=positionsByStates[(
                        CharacterState.IDLE, CharacterDirection.LEFT)],
                    size=self.size,
                    frame_shift=self.frame_shift,
                    fps=self.FPS,
                ),
                (CharacterState.IDLE, CharacterDirection.RIGHT): Animation(
                    sprite_sheet,
                    columns=4,
                    position=positionsByStates[(
                        CharacterState.IDLE, CharacterDirection.RIGHT)],
                    size=self.size,
                    frame_shift=self.frame_shift,
                    fps=self.FPS,
                ),
                (CharacterState.WALKING, CharacterDirection.LEFT): Animation(
                    sprite_sheet,
                    columns=4,
                    position=positionsByStates[(
                        CharacterState.WALKING, CharacterDirection.LEFT)],
                    size=self.size,
                    frame_shift=self.frame_shift,
                    fps=self.FPS,
                ),
                (CharacterState.WALKING, CharacterDirection.RIGHT): Animation(
                    sprite_sheet,
                    columns=4,
                    position=positionsByStates[(
                        CharacterState.WALKING, CharacterDirection.RIGHT)],
                    size=self.size,
                    frame_shift=self.frame_shift,
                    fps=self.FPS,
                ),
                (CharacterState.DYING, CharacterDirection.LEFT): Animation(
                    sprite_sheet,
                    columns=4,
                    position=positionsByStates[(
                        CharacterState.DYING, CharacterDirection.LEFT)],
                    size=self.size,
                    frame_shift=self.frame_shift,
                    fps=self.DYING_FPS,
                    once=True,
                ),
                (CharacterState.DYING, CharacterDirection.RIGHT): Animation(
                    sprite_sheet,
                    columns=4,
                    position=positionsByStates[(
                        CharacterState.DYING, CharacterDirection.RIGHT)],
                    size=self.size,
                    frame_shift=self.frame_shift,
                    fps=self.DYING_FPS,
                    once=True,
                ),
            },
            current,
        )


class Character(pygame.sprite.Sprite):
    def __init__(
        self, position,
        clock: pygame.time.Clock,
        sprite_sheet: AnimationMachine,
        size,
        frame_shift,
        positionsByStates: dict[tuple[CharacterState,
                                      CharacterDirection], tuple[int, int]]
    ):
        super().__init__()
        self.position = pygame.Vector2(position)

        self.direction = CharacterDirection.LEFT
        self.state = CharacterState.IDLE

        self.animation_machine = CharacterAnimationMachine(
            sprite_sheet, (self.state, self.direction),
            positionsByStates, size, frame_shift
        )

        self.image = self.animation_machine.image
        self.rect = self.image.get_rect()

        self.clock = clock

    def update(self):
        self.rect.y = int(self.position.y)
        self.rect.x = int(self.position.x)

        self.select_animation((self.state, self.direction))

        self.animation_machine.update()
        self.image = self.animation_machine.image

    def select_animation(self, key):
        self.animation_machine.select(key)

    @property
    def is_alive(self):
        return self.state != CharacterState.DYING
