import pygame

from utility.events_listener import EventsListener

class Player(pygame.sprite.Sprite, EventsListener):
    def __init__(self, position):
        super().__init__()
        self.position = pygame.Vector2(position)
        
        self.rect = pygame.Rect(self.position.x, self.position.y, 50, 50)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((255, 255, 255))
    
    def update(self):
        self.rect.y = int(self.position.y)
        self.rect.x = int(self.position.x)

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.position.x -= 100
            if event.key == pygame.K_RIGHT:
                self.position.x += 100
            if event.key == pygame.K_UP:
                self.position.y -= 100
            if event.key == pygame.K_DOWN:
                self.position.y += 100