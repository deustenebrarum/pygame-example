from utility.spritesheet import SpriteSheet


class FramedSpriteSheet(SpriteSheet):
  CELL_WIDTH = 24
  CELL_HEIGHT = 24
  
  def __init__(
    self,
    filename,
    scale
  ):
    super().__init__(filename, scale)
  
  def get_frame(
    self, row, column
  ):
    return self.get_image(
      self.CELL_WIDTH * column,
      self.CELL_HEIGHT * row,
      self.CELL_WIDTH,
      self.CELL_HEIGHT
    )