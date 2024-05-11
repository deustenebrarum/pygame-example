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


class Direction(Enum):
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
                (CharacterState.IDLE, Direction.LEFT): Animation(
                    sprite_sheet,
                    columns=4,
                    position=positionsByStates[(
                        CharacterState.IDLE, Direction.LEFT)],
                    size=self.size,
                    frame_shift=self.frame_shift,
                    fps=self.FPS,
                ),
                (CharacterState.IDLE, Direction.RIGHT): Animation(
                    sprite_sheet,
                    columns=4,
                    position=positionsByStates[(
                        CharacterState.IDLE, Direction.RIGHT)],
                    size=self.size,
                    frame_shift=self.frame_shift,
                    fps=self.FPS,
                ),
                (CharacterState.WALKING, Direction.LEFT): Animation(
                    sprite_sheet,
                    columns=4,
                    position=positionsByStates[(
                        CharacterState.WALKING, Direction.LEFT)],
                    size=self.size,
                    frame_shift=self.frame_shift,
                    fps=self.FPS,
                ),
                (CharacterState.WALKING, Direction.RIGHT): Animation(
                    sprite_sheet,
                    columns=4,
                    position=positionsByStates[(
                        CharacterState.WALKING, Direction.RIGHT)],
                    size=self.size,
                    frame_shift=self.frame_shift,
                    fps=self.FPS,
                ),
                (CharacterState.DYING, Direction.LEFT): Animation(
                    sprite_sheet,
                    columns=4,
                    position=positionsByStates[(
                        CharacterState.DYING, Direction.LEFT)],
                    size=self.size,
                    frame_shift=self.frame_shift,
                    fps=self.DYING_FPS,
                    once=True,
                ),
                (CharacterState.DYING, Direction.RIGHT): Animation(
                    sprite_sheet,
                    columns=4,
                    position=positionsByStates[(
                        CharacterState.DYING, Direction.RIGHT)],
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
        direction: Direction = Direction.LEFT,
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

    def set_state(self, state):
        self.state = state
    
    def set_position(self, position):
        if self.state == CharacterState.DYING:
            return

        self.position = pygame.Vector2(position)

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
