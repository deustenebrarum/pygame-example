import random

from enemies.goblin import Goblin
from enemies.skeleton import Skeleton


def random_screen_border_position(
    screen_size: tuple[int, int]
) -> tuple[int, int]:
    axis_choice = random.randint(0, 1)

    if axis_choice == 0:
        return (
            random.randint(0, screen_size[0]),
            random.choice((0, screen_size[1]))
        )

    return (
        random.choice((0, screen_size[0])),
        random.randint(0, screen_size[1])
    )


def random_choice_by_chance(chances: dict):
    return random.choices(
        list(chances.keys()),
        weights=list(chances.values()),
        k=1
    )[0]


def select_random_enemy():
    return random_choice_by_chance({
        Skeleton: 0.3,
        Goblin: 0.9
    })
