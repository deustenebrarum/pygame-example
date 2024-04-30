import pygame

from enemy import Enemy
from player import Player
from utility.events_listener import EventsListener
from utility.random_generators import random_screen_border_position


class Game:
    SCREEN_SIZE = (1280, 720)
    ENEMY_SPAWN_BASE_INTERVAL = 1000

    def __init__(self):
        self.ENEMY_SPAWN_EVENT = pygame.event.custom_type()
        self.enemy_spawn_interval = Game.ENEMY_SPAWN_BASE_INTERVAL

        pygame.init()
        
        self.screen = pygame.display.set_mode(Game.SCREEN_SIZE)

        self.clock = pygame.time.Clock()

        self.events_listeners: list[EventsListener] = []

        pygame.time.set_timer(self.ENEMY_SPAWN_EVENT, Game.ENEMY_SPAWN_BASE_INTERVAL)
        
        self.enemy_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        
        self.player = Player(
            (Game.SCREEN_SIZE[0] / 2, Game.SCREEN_SIZE[1] / 2),
            self.clock,
            self.enemy_group
        )

        self.player_group.add(self.player)


    def draw(self):
        self.player_group.draw(self.screen)
        self.enemy_group.draw(self.screen)

    def run(self):
        is_running = True

        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                
                if event.type == self.ENEMY_SPAWN_EVENT:
                    self.enemy_group.add(Enemy(
                        random_screen_border_position(Game.SCREEN_SIZE), 
                        self.clock, self.player
                    ))
                    if self.enemy_spawn_interval > 300:
                        self.enemy_spawn_interval -= 1
                    else:
                        self.enemy_spawn_interval = 300
                    pygame.time.set_timer(self.ENEMY_SPAWN_EVENT, self.enemy_spawn_interval)
                    

                for listener in self.events_listeners:
                    listener.on_event(event)

            self.player_group.update()

            self.enemy_group.update()

            self.screen.fill((0, 0, 0))

            self.screen.blit(self.screen, (0, 0))

            self.draw()

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
