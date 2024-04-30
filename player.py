from enum import Enum
import pygame

from utility.animation_machine import AnimationMachine
from utility.character import Character
from utility.events_listener import EventsListener
from utility.spritesheet import SpriteSheet
from utility.animation import Animation


class PlayerState(Enum):
    IDLE = 0
    WALKING = 1


class PlayerDirection(Enum):
    LEFT = 0
    RIGHT = 1


class PlayerAnimationMachine(AnimationMachine):
    FPS = 10
    SIZE = (11, 16)
    FRAME_SHIFT = (13, 0)

    def __init__(self, sprite_sheet, current):
        super().__init__(
            {
                (PlayerState.IDLE, PlayerDirection.LEFT): Animation(
                    sprite_sheet,
                    columns=4,
                    position=(103, 9),
                    size=self.SIZE,
                    frame_shift=self.FRAME_SHIFT,
                    fps=self.FPS,
                ),
                (PlayerState.IDLE, PlayerDirection.RIGHT): Animation(
                    sprite_sheet,
                    columns=4,
                    position=(8, 9),
                    size=self.SIZE,
                    frame_shift=self.FRAME_SHIFT,
                    fps=self.FPS,
                ),
                (PlayerState.WALKING, PlayerDirection.LEFT): Animation(
                    sprite_sheet,
                    columns=4,
                    position=(103, 33),
                    size=self.SIZE,
                    frame_shift=self.FRAME_SHIFT,
                    fps=self.FPS,
                ),
                (PlayerState.WALKING, PlayerDirection.RIGHT): Animation(
                    sprite_sheet,
                    columns=4,
                    position=(8, 33),
                    size=self.SIZE,
                    frame_shift=self.FRAME_SHIFT,
                    fps=self.FPS,
                ),
            },
            current,
        )


class Player(Character):
    SPEED = 200
    SPRITE_PATH = "./assets/characters/mHero_.png"
    SCALE = 4

    def __init__(self, position, clock):
        sprite_sheet = SpriteSheet(self.SPRITE_PATH, self.SCALE)

        self.direction = PlayerDirection.LEFT
        self.state = PlayerState.IDLE

        animation_machine = PlayerAnimationMachine(
            sprite_sheet, (self.state, self.direction)
        )

        super().__init__(position, clock, animation_machine)

        self.speed = self.SPEED

    def update(self):
        self._process_control()

        self.select_animation((self.state, self.direction))

        super().update()

    def _process_control(self):
        dt = self.clock.get_time() / 1000
        speed = self.speed * dt

        left_pressed = pygame.key.get_pressed()[pygame.K_LEFT]
        right_pressed = pygame.key.get_pressed()[pygame.K_RIGHT]
        up_pressed = pygame.key.get_pressed()[pygame.K_UP]
        down_pressed = pygame.key.get_pressed()[pygame.K_DOWN]

        if left_pressed:
            self.state = PlayerState.WALKING
            self.direction = PlayerDirection.LEFT
            self.position.x -= speed
        if right_pressed:
            self.state = PlayerState.WALKING
            self.direction = PlayerDirection.RIGHT
            self.position.x += speed
        if up_pressed:
            self.state = PlayerState.WALKING
            self.position.y -= speed
        if down_pressed:
            self.state = PlayerState.WALKING
            self.position.y += speed

        if not any((
            left_pressed,
            right_pressed,
            up_pressed,
            down_pressed
        )):
            self.state = PlayerState.IDLE
            if self.animation_machine.is_current((PlayerState.WALKING, PlayerDirection.LEFT)):
                self.direction = PlayerDirection.LEFT
            elif self.animation_machine.is_current((PlayerState.WALKING, PlayerDirection.RIGHT)):
                self.direction = PlayerDirection.RIGHT
