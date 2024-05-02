import random
from .goblin_spritesheet import GoblinSpriteSheet
from .skeleton_spritesheet import SkeletonSpriteSheet
from utility.spritesheet import SpriteSheet

__all__ = [
    "GoblinSpriteSheet",
    "SkeletonSpriteSheet",
]


def get_random_sprite_sheet() -> SpriteSheet:
    SPRITE_SHEETS = [
        GoblinSpriteSheet(),
        SkeletonSpriteSheet(),
    ]

    return random.choice(SPRITE_SHEETS)
