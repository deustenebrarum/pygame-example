import pygame

class Game:
    SCREEN_SIZE = (1280, 720)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Game.SCREEN_SIZE)
        
        self.clock = pygame.time.Clock()

    def run(self):
        is_running = True

        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

            self.screen.fill((0, 0, 0))
            
            pygame.display.flip()
            
            self.clock.tick(60)

        pygame.quit()