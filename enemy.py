

import pygame
from utility.character import Character, CharacterDirection, CharacterState
from utility.spritesheet import SpriteSheet


class Enemy(Character):
    SPEED = 100
    SPRITE_PATH = "./assets/characters/goblin_.png"
    SCALE = 4
    LIFE_LIMIT = 1000 * 5
    
    def __init__(self, position, clock, player):
        sprite_sheet = SpriteSheet(self.SPRITE_PATH, self.SCALE)
        
        super().__init__(
            position, clock, sprite_sheet,
            positionsByStates={
                (CharacterState.IDLE, CharacterDirection.RIGHT): (6, 8),
                (CharacterState.IDLE, CharacterDirection.LEFT): (103, 8),
                (CharacterState.WALKING, CharacterDirection.RIGHT): (6, 32),
                (CharacterState.WALKING, CharacterDirection.LEFT): (103, 32),
            }
        )
        
        self.player = player
        
        self.speed = self.SPEED
        self.spawn_time = pygame.time.get_ticks()
        self.state = CharacterState.WALKING
    
    def update(self):
        self.move_to_player(self.player)
        
        if pygame.time.get_ticks() - self.spawn_time > self.LIFE_LIMIT:
            self.kill()
        
        super().update()
    
    def move_to_player(self, player):
        dt = self.clock.get_time() / 1000
        speed = self.speed * dt
        
        vector = pygame.Vector2(player.position) - pygame.Vector2(self.position)
        if vector.x < 0:
            self.direction = CharacterDirection.LEFT
        else:
            self.direction = CharacterDirection.RIGHT
        self.position += vector.normalize() * speed

