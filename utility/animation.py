import pygame

from utility.spritesheet import SpriteSheet


class Animation:
    def __init__(
        self, sprite_sheet: SpriteSheet, columns,
        position,
        size, frame_shift, fps,
        once=False
    ):
        self.sprite_sheet = sprite_sheet
        self.columns = columns
        self.once = once

        self.fps = fps
        self._last_update = pygame.time.get_ticks()
        self._frame = 0
        self._animation_start = pygame.time.get_ticks()
        self._position = position
        self._size = size
        self._frame_shift = frame_shift
        shifts = (
            (
                position[0] + (frame_shift[0] + size[0]) * column,
                position[1]
            )
            for column in range(columns)
        )
        self.frames = [
            self._get_frame(position, size)
            for position in shifts
        ]

    def change_params(self, 
        sprite_sheet=None, columns=None, 
        position=None, 
        size=None, frame_shift=None, fps=None, 
        once=None
    ):
        if sprite_sheet is not None:
            self.sprite_sheet = sprite_sheet
        if columns is not None:
            self.columns = columns
        if once is not None:
            self.once = once
        if size is not None:
            self._size = size
        if frame_shift is not None:
            self._frame_shift = frame_shift
        if fps is not None:
            self.fps = fps
        if position is not None:
            self._position = position

        self._last_update = pygame.time.get_ticks()
        self._frame = 0
        self._animation_start = pygame.time.get_ticks()
         
        shifts = (
            (
                self._position[0] + (self._frame_shift[0] + self._size[0]) * column,
                self._position[1]
            )
            for column in range(self.columns)
        )
        self.frames = [
            self._get_frame(self._position, self._size)
            for self._position in shifts
        ]

        
    
    @property
    def image(self):
        return self.frames[self._frame]

    def start(self):
        self._frame = 0
        self._animation_start = pygame.time.get_ticks()
        self._last_update = pygame.time.get_ticks()

    def update(self):
        if self.once and self._frame == len(self.frames) - 1:
            return
        now = pygame.time.get_ticks()
        if now - self._last_update > 1000 / self.fps:
            self._frame = (self._frame + 1) % len(self.frames)
            self._last_update = now

    @property
    def ended_once(self):
        now = pygame.time.get_ticks()
        if now - self._animation_start >= len(self.frames) * 1000 / self.fps:
            return True
        return False

    @property
    def ended(self):
        return self._frame == len(self.frames) - 1

    def _get_frame(self, position, size):
        return self.sprite_sheet.get_image(
            position[0], position[1],
            size[0], size[1]
        )
