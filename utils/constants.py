from enum import Enum
from pathlib import Path
from collections.abc import Sequence, Callable
from typing import Annotated, TypedDict


class Kind(Enum):
    CAT = 'cat'
    DOG = 'dog'
    FOX = 'fox'
    BEAR = 'bear'
    SNAKE = 'snake'
    LIZARD = 'lizard'
    TURTLE = 'turtle'
    # ...


class Matureness(str, Enum):
    EGG = 'egg'
    CUB = 'cub'
    YOUNG = 'young'
    ADULT = 'adult'
    ELDER = 'elder'

    @classmethod
    def mammals(cls):
        res = list(cls)
        res.remove(cls.EGG)
        return res


pathlike = str | Path

KindActions = dict[Kind, Sequence[Callable]]
ParamRanges = Sequence[Annotated[Sequence[int], 2]]
RangesDict = TypedDict('RangesDict', {
    'health': ParamRanges,
    'stamina': ParamRanges,
    'hunger': ParamRanges,
    'thirst': ParamRanges
})
MatureDays = Annotated[Sequence[int], 3] | Annotated[Sequence[int], 4]

