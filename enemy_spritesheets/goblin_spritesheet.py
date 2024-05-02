from utility.spritesheet import SpriteSheet


class GoblinSpriteSheet(SpriteSheet):
    SPRITE_PATH = "./assets/characters/goblin_.png"
    SCALE = 4

    def __init__(self):
        super().__init__(self.SPRITE_PATH, self.SCALE)
