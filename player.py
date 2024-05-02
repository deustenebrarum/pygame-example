import pygame

from utility.character import Character, CharacterDirection, CharacterState
from utility.spritesheet import SpriteSheet


class Player(Character):
    SPEED = 200
    SPRITE_PATH = "./assets/characters/mHero_.png"
    SCALE = 4

    def __init__(self, position, clock, enemy_group):
        sprite_sheet = SpriteSheet(self.SPRITE_PATH, self.SCALE)

        super().__init__(
            position, clock, sprite_sheet,
            (11, 16), (13, 0),
            positionsByStates={
                (CharacterState.IDLE, CharacterDirection.LEFT): (103, 9),
                (CharacterState.IDLE, CharacterDirection.RIGHT): (8, 9),
                (CharacterState.WALKING, CharacterDirection.LEFT): (103, 33),
                (CharacterState.WALKING, CharacterDirection.RIGHT): (8, 33),
                (CharacterState.DYING, CharacterDirection.RIGHT): (8, 152),
                (CharacterState.DYING, CharacterDirection.LEFT): (103, 152),
            }
        )

        self.speed = self.SPEED
        self.enemy_group = enemy_group
        self.invulnerable = False

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
