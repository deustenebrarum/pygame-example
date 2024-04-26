import pygame

from utility.events_listener import EventsListener

class Player(pygame.sprite.Sprite, EventsListener):
    def __init__(self, position):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((255, 255, 255))
        self.position = pygame.Vector2(position)
    
    def update(self):
        pass

    def on_event(self, event):
        if event.key == pygame.K_LEFT:
            self.position.x -= 1
        if event.key == pygame.K_RIGHT:
            self.position.x += 1
        if event.key == pygame.K_UP:
            self.position.y -= 1
        if event.key == pygame.K_DOWN:
            self.position.y += 1