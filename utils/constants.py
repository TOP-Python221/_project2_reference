__all__ = [
    'Kind'
]

from enum import Enum
from pathlib import Path
from sys import path
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
    CUB = 'cub'
    YOUNG = 'young'
    ADULT = 'adult'
    ELDER = 'elder'


BASE_DIR = Path(path[0])


pathlike = str | Path

KindActions = dict[Kind, Sequence[Callable]]
ParamRange = Annotated[Sequence[float], 2]
ParamRanges = Sequence[ParamRange]
ParamRangesInfluences = dict[str, dict[str, float]]
RangesDict = TypedDict('RangesDict', {
    'health': ParamRangesInfluences,
    'stamina': ParamRangesInfluences,
    'hunger': ParamRangesInfluences,
    'thirst': ParamRangesInfluences,
    'intestine': ParamRangesInfluences,
    'activity': ParamRanges,
    'anxiety': ParamRanges,
    'anger_coeff': float,
    'joy_coeff': float,
})
MatureDays = Annotated[Sequence[int], 3] | Annotated[Sequence[int], 4]

