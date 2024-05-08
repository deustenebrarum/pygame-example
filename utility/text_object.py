import pygame


class TextObject:
    def __init__(self, text, font=None, color=(255, 255, 255)):
        if font is None:
            font = pygame.font.SysFont("Arial", 16)

        self._text = text
        self._font = font
        self._color = color

        self.surface = self._font.render(self._text, True, self._color)

    def draw(self, surface: pygame.surface.Surface, destination: tuple[int, int]):
        surface.blit(self.surface, destination)

    def change_text(self, text):
        self._text = text

        self.surface = self._font.render(self._text, True, self._color)

    def get_width(self):
        return self.surface.get_width()

    def get_height(self):
        return self.surface.get_height()