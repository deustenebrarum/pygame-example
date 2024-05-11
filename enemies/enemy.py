import pygame
from utility.character import Character, Direction, CharacterState


class Enemy(Character):
    def __init__(
        self, position, clock, player,
        animation_machine,
        collision_size: tuple[int, int],
        life_limit=1000 * 4,
        speed=Character.BASE_SPEED
    ):
        self.life_limit = life_limit

        super().__init__(
            position, clock, animation_machine,
            collision_size,
            CharacterState.WALKING, Direction.RIGHT,
            speed=speed
        )

        self.player = player

        self.speed = self.speed
        self.spawned_time = pygame.time.get_ticks()
        self.state = CharacterState.WALKING

    def update(self):
        if self.is_alive:
            self.move_to_player(self.player)

        if pygame.time.get_ticks() - self.spawned_time > self.life_limit:
            self.state = CharacterState.DYING

        super().update()

        if (
            (not self.is_alive) and
            self.animation_machine.animation.ended_once
        ):
            self.kill()

    def move_to_player(self, player):
        dt = self.clock.get_time() / 1000
        speed = self.speed * dt

        vector = (
            player.position -
            self.position
        )
        if vector.x < 0:
            self.direction = Direction.LEFT
        else:
            self.direction = Direction.RIGHT
        self.position += vector.normalize() * speed
