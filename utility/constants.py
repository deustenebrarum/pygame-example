from enum import Enum


PIXELS_PER_UNIT = 4
MAX_GAME_TIME = 1 * 60 * 1000

class GameOverState(Enum):
  QUIT = 0
  LOSE = 1
  WIN = 2
