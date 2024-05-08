from enum import Enum
import pygame

from utility.animation import Animation
from utility.animation_machine import AnimationMachine
from utility.collision_box import CollisionBox
from utility import constants


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
        positionsByStates, size=(24, 24), frame_shift=(0, 0)
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
    BASE_SPEED = 200

    def __init__(
        self, position: tuple[int, int],
        clock: pygame.time.Clock,
        animation_machine: AnimationMachine,
        collision_size: tuple[int, int],
        state: CharacterState = CharacterState.IDLE,
        direction: CharacterDirection = CharacterDirection.LEFT,
        collision_offset: tuple[int, int] = (
            0, 4 * constants.PIXELS_PER_UNIT
        ),
        speed=BASE_SPEED
    ):
        super().__init__()
        self.speed = speed
        self.position = pygame.Vector2(position)
        self.collision_offset = pygame.Vector2(collision_offset)

        self.collision_box = CollisionBox(
            (position[0] + collision_offset[0],
             position[1] + collision_offset[1]),
            collision_size
        )

        self.direction = direction
        self.state = state

        self.animation_machine = animation_machine

        self.image = self.animation_machine.image

        self.rect = self.image.get_rect()

        self.clock = clock

    def update(self):
        self.rect.y = int(self.edge_position.y)
        self.rect.x = int(self.edge_position.x)
        self.collision_box.x = int(
            self.position.x +
            self.collision_offset.x -
            self.collision_box.width / 2
        )
        self.collision_box.y = int(
            self.position.y +
            self.collision_offset.y -
            self.collision_box.height / 2
        )

        self.select_animation((self.state, self.direction))

        self.animation_machine.update()
        self.image = self.animation_machine.image

    @property
    def edge_position(self):
        return pygame.Vector2(
            self.position.x - self.rect.width / 2,
            self.position.y - self.rect.height / 2
        )

    def select_animation(self, key):
        self.animation_machine.select(key)

    @property
    def is_alive(self):
        return self.state != CharacterState.DYING
