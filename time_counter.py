import pygame

from utility.text_object import TextObject


class TimeCounter:
    def __init__(self, clock: pygame.time.Clock, max_game_time):
        font = pygame.font.SysFont("Arial", 50, bold=True)
        self.text = TextObject("", font=font)
        self.clock = clock

        self.max_time = max_game_time
        self._time_left = max_game_time

    def start(self):
        self._time_left = self.max_time
        self.update_text(self._time_left)

    def update(self):
        if self._time_left > 0:
            self._time_left -= self.clock.get_time()
        else:
            self._time_left = 0
        self.update_text(self._time_left)

    @property
    def is_over(self):
        return self._time_left <= 0

    def update_text(self, time_left):
        minutes = time_left // (60 * 1000)
        seconds = (time_left % (60 * 1000)) // 1000
        self.text.change_text(f"TIME LEFT: {minutes}:{seconds}")

    def draw(self, surface: pygame.surface.Surface):
        center = surface.get_width() // 2 - self.text.get_width() // 2
        self.text.draw(surface, (center, 0))
