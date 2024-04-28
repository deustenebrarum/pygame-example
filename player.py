import pygame

from utility.events_listener import EventsListener

class Player(pygame.sprite.Sprite, EventsListener):
    def __init__(self, position):
        super().__init__()
        self.position = pygame.Vector2(position)
        
        self.rect = pygame.Rect(self.position.x, self.position.y, 50, 50)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((255, 255, 255))

        self.speed = 5
    
    def update(self):
        self._process_control()

        self.rect.y = int(self.position.y)
        self.rect.x = int(self.position.x)

    def _process_control(self):
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.position.x -= self.speed
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.position.x += self.speed
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.position.y -= self.speed
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.position.y += self.speed

    def on_event(self, event):
        pass