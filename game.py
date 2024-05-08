import pygame

from player import Player
from time_counter import TimeCounter
from utility.constants import GameOverState, MAX_GAME_TIME
from utility.events_listener import EventsListener
from utility.random_generators import (
    random_screen_border_position,
    select_random_enemy
)


class Game:
    SCREEN_SIZE = (1600, 900)
    ENEMY_SPAWN_BASE_INTERVAL = 1000
    INTERVAL_DELTA = ENEMY_SPAWN_BASE_INTERVAL // 3 * \
        2 // (MAX_GAME_TIME // 1000)

    def __init__(self, debug=False):
        self.debug = debug

        self.ENEMY_SPAWN_EVENT = pygame.event.custom_type()
        self.enemy_spawn_interval = Game.ENEMY_SPAWN_BASE_INTERVAL

        pygame.init()

        self.screen = pygame.display.set_mode(Game.SCREEN_SIZE)

        self.clock = pygame.time.Clock()

        self.events_listeners: list[EventsListener] = []

        pygame.time.set_timer(
            self.ENEMY_SPAWN_EVENT,
            Game.ENEMY_SPAWN_BASE_INTERVAL
        )

        self.enemy_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()

        self.player = Player(
            (Game.SCREEN_SIZE[0] / 2, Game.SCREEN_SIZE[1] / 2),
            self.clock,
            self.enemy_group
        )

        self.player_group.add(self.player)

        self.time_counter = TimeCounter(self.clock)
        self.is_running = True

    def _draw_debug(self):
        def draw_collisions(characters):
            for character in characters:
                pygame.draw.rect(
                    self.screen,
                    (255, 0, 0),
                    character.collision_box
                )

        draw_collisions(self.player_group)
        draw_collisions(self.enemy_group)

    def draw(self):
        if self.debug:
            self._draw_debug()

        self.time_counter.draw(self.screen)

        self.player_group.draw(self.screen)

        self.enemy_group.draw(self.screen)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if event.type == self.ENEMY_SPAWN_EVENT:
                self.enemy_group.add(select_random_enemy()(
                    random_screen_border_position(Game.SCREEN_SIZE),
                    self.clock, self.player
                ))
                if self.enemy_spawn_interval > 300:
                    dt = self.clock.get_time() / 1000
                    self.enemy_spawn_interval -= self.INTERVAL_DELTA * dt
                else:
                    self.enemy_spawn_interval = 300
                pygame.time.set_timer(
                    self.ENEMY_SPAWN_EVENT, int(self.enemy_spawn_interval))

            for listener in self.events_listeners:
                listener.on_event(event)

    def update(self):
        self.player_group.update()

        self.player.collide_borders(
            self.screen.get_width(),
            self.screen.get_height()
        )

        self.enemy_group.update()

        self.time_counter.update()

    def on_game_over_loop(self, game_over_state: GameOverState):
        self.process_events()

        font = pygame.font.SysFont("Arial", 50, bold=True)
        
        game_over_text = "YOU LOSE"
        if game_over_state == GameOverState.WIN:
            game_over_text = "YOU WIN"
            self.screen.fill((0, 0, 0))

        text = font.render(game_over_text, True, (255, 255, 255))
        self.screen.blit(
            text,
            (
                Game.SCREEN_SIZE[0] / 2 - text.get_width() / 2,
                Game.SCREEN_SIZE[1] / 2 - text.get_height() / 2
            )
        )

        pygame.display.flip()

    def run(self):
        game_over_state = GameOverState.QUIT

        self.time_counter.start()

        while self.is_running:
            self.process_events()

            self.update()

            self.screen.fill((0, 0, 0))

            self.draw()

            if not self.player.alive():
                self.is_running = False
                game_over_state = GameOverState.LOSE

            if self.time_counter.is_over:
                self.is_running = False
                game_over_state = GameOverState.WIN

            pygame.display.flip()

            self.clock.tick(60)

        if game_over_state == GameOverState.QUIT:
            pygame.quit()
            return

        pygame.event.clear(self.ENEMY_SPAWN_EVENT)
        self.is_running = True

        while self.is_running:
            self.on_game_over_loop(game_over_state)

        pygame.quit()
