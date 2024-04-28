import pygame

from utility.spritesheet import SpriteSheet

class Animation:
    def __init__(self, sprite_sheet: SpriteSheet, columns, fps, position, size, frame_shift):
        self.sprite_sheet = sprite_sheet
        self.columns = columns
        
        self.fps = fps
        self.last_update = 0
        self.frame = 0
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
    
    def _get_frame(self, position, size):
        return self.sprite_sheet.get_image(
            position[0], position[1], 
            size[0], size[1]
        )