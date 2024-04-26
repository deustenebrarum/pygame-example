import pygame

from player import Player
from utility.events_listener import EventsListener


class Game:
    SCREEN_SIZE = (1280, 720)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Game.SCREEN_SIZE)

        self.clock = pygame.time.Clock()
        
        self.surface = pygame.Surface(Game.SCREEN_SIZE)

        self.player = Player(
            (Game.SCREEN_SIZE[0] / 2, Game.SCREEN_SIZE[1] / 2)
        )
        
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
    
    def draw(self):
        self.player_group.draw()

    def run(self):
        is_running = True

        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                EventsListener.dispatch(event)

            self.screen.fill((0, 0, 0))

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
