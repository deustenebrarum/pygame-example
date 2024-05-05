import pygame
from utility.character import Character, CharacterDirection, CharacterState

class Enemy(Character):
    def __init__(
        self, position, clock, player,
        animation_machine,
        collision_size: tuple[int, int],
        life_limit = 1000 * 4,
        speed = 100
    ):
        self.life_limit = life_limit
        self.speed = speed
        
        super().__init__(
            position, clock, animation_machine,
            collision_size,
            CharacterState.WALKING, CharacterDirection.RIGHT
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
            pygame.Vector2(player.position) -
            pygame.Vector2(self.position)
        )
        if vector.x < 0:
            self.direction = CharacterDirection.LEFT
        else:
            self.direction = CharacterDirection.RIGHT
        self.position += vector.normalize() * speed
