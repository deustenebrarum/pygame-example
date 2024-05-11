import pygame

from sword import Sword
from utility.character import (
    Character, CharacterAnimationMachine,
    Direction, CharacterState
)
from utility.framed_spritesheet import FramedSpriteSheet


class PlayerAnimationMachine(CharacterAnimationMachine):
    SPRITE_PATH = "./assets/characters/mHero_.png"

    def __init__(self):
        sprite_sheet = FramedSpriteSheet(self.SPRITE_PATH)

        UNIT_PX = 24

        super().__init__(
            sprite_sheet, (CharacterState.IDLE, Direction.LEFT),
            {
                (CharacterState.IDLE, Direction.LEFT): (
                    UNIT_PX*4 + 1, 0
                ),
                (CharacterState.IDLE, Direction.RIGHT): (
                    0, 0
                ),
                (CharacterState.WALKING, Direction.LEFT): (
                    UNIT_PX*4 + 1, UNIT_PX + 1
                ),
                (CharacterState.WALKING, Direction.RIGHT): (
                    0, 25
                ),
                (CharacterState.DYING, Direction.RIGHT): (
                    UNIT_PX * 4 + 1, UNIT_PX * 2 + 1
                ),
                (CharacterState.DYING, Direction.LEFT): (
                    0, 49
                ),
            }
        )


class Player(Character):
    def __init__(self, position, clock, enemy_group, weapon):

        animation_machine = PlayerAnimationMachine()

        super().__init__(
            position, clock,
            animation_machine,
            collision_size=(32, 50),
        )

        self.enemy_group = enemy_group
        self.invulnerable = False

        self.weapon = weapon

    def update(self):
        self._process_collision()
        self._process_control()

        self.weapon.update()
        self.weapon.set_position(self.position)

        super().update()

    def _process_collision(self):
        if self.invulnerable:
            return

        collided_enemies = [
            enemy
            for enemy in self.enemy_group
            if enemy.collision_box.collides_with(self.collision_box)
        ]

        any_enemy_alive = any([enemy.is_alive for enemy in collided_enemies])
        if any_enemy_alive:
            self.kill()
    
    def collide_borders(self, width, height):
        if self.collision_box.right >= width:
            self.position.x = width - self.collision_box.width / 2
        if self.collision_box.left <= 0:
            self.position.x = self.collision_box.width / 2
        if self.collision_box.top <= 0:
            self.position.y = self.collision_box.height / 2 - self.collision_offset.y
        if self.collision_box.bottom >= height:
            self.position.y = height - self.collision_box.height / 2 - self.collision_offset.y

    def _process_control(self):
        dt = self.clock.get_time() / 1000
        speed = self.speed * dt

        left_pressed = pygame.key.get_pressed()[pygame.K_LEFT]
        right_pressed = pygame.key.get_pressed()[pygame.K_RIGHT]
        up_pressed = pygame.key.get_pressed()[pygame.K_UP]
        down_pressed = pygame.key.get_pressed()[pygame.K_DOWN]

        if left_pressed:
            self.state = CharacterState.WALKING
            self.direction = Direction.LEFT
            self.position.x -= speed
        if right_pressed:
            self.state = CharacterState.WALKING
            self.direction = Direction.RIGHT
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

    def kill(self):
        self.weapon.kill()
        super().kill()