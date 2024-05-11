from enum import Enum


PIXELS_PER_UNIT = 4

class GameOverState(Enum):
  QUIT = 0
  LOSE = 1
  WIN = 2
