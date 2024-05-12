import pygame

from player import Player
from sword import Sword
from time_counter import TimeCounter
from utility.character import CharacterState
from utility.constants import GameOverState
from utility.events_listener import EventsListener
from utility.random_generators import (
    random_screen_border_position,
    select_random_enemy
)


class Game:
    SCREEN_SIZE = (1600, 900)
    BASE_ROOM_TIME = 1 * 10 * 1000
    ENEMY_SPAWN_BASE_INTERVAL = 800
    ENEMY_SPAWN_LIMIT_INTERVAL = 300

    def __init__(self, debug=False):
        self.debug = debug
        self.room_time = Game.BASE_ROOM_TIME
        self.level = 1

        self.ENEMY_SPAWN_EVENT = pygame.event.custom_type()
        self.enemy_spawn_interval = Game.ENEMY_SPAWN_BASE_INTERVAL

        pygame.init()

        self.screen = pygame.display.set_mode(Game.SCREEN_SIZE)

        self.clock = pygame.time.Clock()

        self.events_listeners: list[EventsListener] = []

        pygame.time.set_timer(
            self.ENEMY_SPAWN_EVENT,
            self.enemy_spawn_interval
        )

        self.enemy_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.weapon_group = pygame.sprite.Group()

        self.weapon = Sword((Game.SCREEN_SIZE[0] / 2, Game.SCREEN_SIZE[1] / 2))

        self.weapon_group.add(self.weapon)

        self.player = Player(
            (Game.SCREEN_SIZE[0] / 2, Game.SCREEN_SIZE[1] / 2),
            self.clock,
            self.enemy_group,
            self.weapon
        )

        self.player_group.add(self.player)

        self.time_counter = TimeCounter(self.clock, self.room_time)
        self.is_running = True

        self.is_level_over = False

    def start_next_level(self):
        self.level += 1
        self.room_time = self.BASE_ROOM_TIME
        interval_diff = 100
        if self.enemy_spawn_interval - interval_diff > self.ENEMY_SPAWN_LIMIT_INTERVAL:
            self.enemy_spawn_interval -= interval_diff
            pygame.time.set_timer(self.ENEMY_SPAWN_EVENT,
                                  self.enemy_spawn_interval)

        self.time_counter.start()
        self.is_level_over = False
        self.player.position = pygame.Vector2(
            self.player.collision_box.width*3,
            self.player.position.y
        )

    def finish_level(self):
        self.stop_spawning()
        self.is_level_over = True

    def stop_spawning(self):
        pygame.time.set_timer(
            self.ENEMY_SPAWN_EVENT,
            0
        )

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
        draw_collisions(self.weapon_group)

    def draw(self):
        if self.debug:
            self._draw_debug()

        self.time_counter.draw(self.screen)

        self.enemy_group.draw(self.screen)

        self.player_group.draw(self.screen)

        self.weapon_group.draw(self.screen)

    def process_events(self, is_game_over=False):
        for event in pygame.event.get():
            if is_game_over and event.type == pygame.constants.KEYDOWN:
                self.is_running = False

            if event.type == pygame.QUIT:
                self.is_running = False

            if event.type == self.ENEMY_SPAWN_EVENT:
                self.enemy_group.add(select_random_enemy()(
                    random_screen_border_position(Game.SCREEN_SIZE),
                    self.clock, self.player
                ))

            for listener in self.events_listeners:
                listener.on_event(event)

    def collide_borders(self):
        if (
            not self.is_next_level_allowed() and
            self.player.collision_box.right >= self.SCREEN_SIZE[0]
        ):
            self.player.position.x = (
                Game.SCREEN_SIZE[0] -
                self.player.collision_box.width / 2
            )
        if self.player.collision_box.left <= 0:
            self.player.position.x = self.player.collision_box.width / 2
        if self.player.collision_box.top <= 0:
            self.player.position.y = (
                self.player.collision_box.height / 2 -
                self.player.collision_offset.y
            )
        if self.player.collision_box.bottom >= Game.SCREEN_SIZE[1]:
            self.player.position.y = (
                Game.SCREEN_SIZE[1] - self.player.collision_box.height / 2 -
                self.player.collision_offset.y
            )
    
    def is_next_level_allowed(self):
        return (
            self.time_counter.is_over and
            len(self.enemy_group.sprites()) == 0
        )

    def update(self):
        self.player_group.update()

        self.collide_borders()

        self.enemy_group.update()

        self.time_counter.update()

        for enemy in pygame.sprite.spritecollide(
            self.weapon,
            self.enemy_group,
            False
        ):
            pos_diff = enemy.position - self.player.position
            enemy.set_position((
                enemy.position.x + (-30 if pos_diff.x < 0 else 30),
                enemy.position.y
            ))
            enemy.set_state(CharacterState.DYING)

    def on_game_over_loop(self, game_over_state: GameOverState):
        self.process_events(is_game_over=True)

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

            if (
                self.is_next_level_allowed() and
                self.player.position.x > self.SCREEN_SIZE[0] +
                    self.player.collision_box.width / 2
            ):
                self.start_next_level()

            self.update()

            self.screen.fill((0, 0, 0))

            self.draw()

            if not self.player.alive():
                self.is_running = False
                game_over_state = GameOverState.LOSE

            if not self.is_level_over and self.time_counter.is_over:
                self.finish_level()

            pygame.display.flip()

            self.clock.tick(60)

        if game_over_state == GameOverState.QUIT:
            pygame.quit()
            return

        self.stop_spawning()
        self.is_running = True

        while self.is_running:
            self.on_game_over_loop(game_over_state)

        pygame.quit()
