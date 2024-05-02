from utility.spritesheet import SpriteSheet


class SkeletonSpriteSheet(SpriteSheet):
    SPRITE_PATH = "./assets/characters/skeleton_.png"
    SCALE = 4

    def __init__(self):
        super().__init__(self.SPRITE_PATH, self.SCALE)
