import pygame

from utility.character import Character, CharacterAnimationMachine, CharacterDirection, CharacterState
from utility.spritesheet import SpriteSheet


class PlayerAnimationMachine(CharacterAnimationMachine):
    SPRITE_PATH = "./assets/characters/mHero_.png"
    SCALE = 4
    SIZE = (11, 16)
    FRAME_SHIFT = (13, 0)

    def __init__(self):
        sprite_sheet = SpriteSheet(self.SPRITE_PATH, self.SCALE)

        super().__init__(
            sprite_sheet, (CharacterState.IDLE, CharacterDirection.LEFT),
            {
                (CharacterState.IDLE, CharacterDirection.LEFT): (103, 9),
                (CharacterState.IDLE, CharacterDirection.RIGHT): (8, 9),
                (CharacterState.WALKING, CharacterDirection.LEFT): (103, 33),
                (CharacterState.WALKING, CharacterDirection.RIGHT): (8, 33),
                (CharacterState.DYING, CharacterDirection.RIGHT): (8, 152),
                (CharacterState.DYING, CharacterDirection.LEFT): (103, 152),
            },
            self.SIZE, self.FRAME_SHIFT
        )


class Player(Character):
    BASE_SPEED = 200

    def __init__(self, position, clock, enemy_group):

        animation_machine = PlayerAnimationMachine()

        super().__init__(
            position, clock,
            animation_machine
        )

        self.speed = self.BASE_SPEED
        self.enemy_group = enemy_group
        self.invulnerable = True

    def update(self):
        self._process_collision()
        self._process_control()

        super().update()

    def _process_collision(self):
        if self.invulnerable:
            return

        collided_enemies = pygame.sprite.spritecollide(
            self, self.enemy_group, False
        )
        any_enemy_alive = any([enemy.is_alive for enemy in collided_enemies])
        if len(collided_enemies) > 0 and any_enemy_alive:
            self.kill()

    def _process_control(self):
        dt = self.clock.get_time() / 1000
        speed = self.speed * dt

        left_pressed = pygame.key.get_pressed()[pygame.K_LEFT]
        right_pressed = pygame.key.get_pressed()[pygame.K_RIGHT]
        up_pressed = pygame.key.get_pressed()[pygame.K_UP]
        down_pressed = pygame.key.get_pressed()[pygame.K_DOWN]

        if left_pressed:
            self.state = CharacterState.WALKING
            self.direction = CharacterDirection.LEFT
            self.position.x -= speed
        if right_pressed:
            self.state = CharacterState.WALKING
            self.direction = CharacterDirection.RIGHT
            self.position.x += speed
        if up_pressed:
            self.state = CharacterState.WALKING
            self.position.y -= speed
        if down_pressed:
            self.state = CharacterState.WALKING
            self.position.y += speed

        if not any((
            left_pressed,
            right_pressed,
            up_pressed,
            down_pressed
        )):
            self.state = CharacterState.IDLE
            if self.animation_machine.is_current(
                (CharacterState.WALKING, CharacterDirection.LEFT)
            ):
                self.direction = CharacterDirection.LEFT
            elif self.animation_machine.is_current(
                (CharacterState.WALKING, CharacterDirection.RIGHT)
            ):
                self.direction = CharacterDirection.RIGHT
