import random


def random_screen_border_position(screen_size: tuple[int, int]) -> tuple[int, int]:
    axis_choice = random.randint(0, 1)

    if axis_choice == 0:
        return (random.randint(0, screen_size[0]), random.choice((0, screen_size[1])))
    else:
        return (random.choice((0, screen_size[0])), random.randint(0, screen_size[1]))
