from typing import Generic, TypeVar
from utility.animation import Animation

T = TypeVar('T')


class AnimationMachine(Generic[T]):
    def __init__(self, animations: dict[T, Animation], current: T) -> None:
        self.animations = animations
        self.animation = self.animations[current]
        self.animation.start()

    def select(self, key: T):
        if self.animations[key] == self.animation:
            return

        self.animation = self.animations[key]

        self.animation.start()

    def update(self) -> None:
        self.animation.update()

    @property
    def image(self):
        return self.animation.image

    def is_current(self, key: T) -> bool:
        return self.animation == self.animations[key]
