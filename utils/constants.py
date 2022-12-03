from enum import Enum
from typing import Callable
from pathlib import Path


class Kind(Enum):
    CAT = 'кошка'
    DOG = 'собака'
    FOX = 'лиса'
    BEAR = 'медведь'
    SNAKE = 'змея'
    LIZARD = 'ящерица'
    TURTLE = 'черепаха'
    # ...


pathlike = str | Path
KindActions = dict[Kind, tuple[Callable]]


