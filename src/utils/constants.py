__all__ = [
    'Kind',
    'DEBUG'
]

# импорт из стандартной библиотеки
from collections.abc import Sequence, Callable
from enum import Enum
from pathlib import Path
from re import compile as reg_pattern_compile
from sys import path
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
SOURCE_DIR = BASE_DIR / 'src'
DATA_DIR = BASE_DIR / 'data'

DEBUG = False

separated_floats_pattern = reg_pattern_compile(
    r'^((?P<float>\d+\.\d+)(?P<sep>[,; ])?){2,}$'
)


pathlike = str | Path
Actions = Sequence[Callable]
KindActions = dict[Kind, Actions]
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


ACTIVE_STATE_KEY = 'last_state'
ACTIVE_KEYS = {'kind', 'name', 'birthdate', ACTIVE_STATE_KEY}
ACTIVE_STATE_KEYS = {'timestamp', 'health', 'stamina', 'hunger', 'thirst', 'intestine', 'joy', 'activity', 'anger', 'anxiety'}
