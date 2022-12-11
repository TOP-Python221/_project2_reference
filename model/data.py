__all__ = [
    'KindParameters',
    'State',
]

# импорт из стандартной библиотеки
from dataclasses import dataclass
from datetime import datetime as dt
from itertools import pairwise

# импорт дополнительных модулей других пакетов
import utils.constants as uc
import utils.types as ut


class KindParameters:
    """

    """
    class Ranges:
        def __init__(self, health_ranges, stamina_ranges, hunger_ranges, thirst_ranges, intestine_ranges, activity, anxiety, anger_coeff, joy_coeff):
            self.health: ut.DictOfRanges = health_ranges
            self.stamina: ut.DictOfRanges = stamina_ranges
            self.hunger: ut.DictOfRanges = hunger_ranges
            self.thirst: ut.DictOfRanges = thirst_ranges
            self.intestine: ut.DictOfRanges = intestine_ranges
            self.joy: uc.ParamRange = (0, 100)
            self.joy_coeff: float = joy_coeff
            self.activity: uc.ParamRange = activity
            self.anger: uc.ParamRange = (0, 100)
            self.anger_coeff: float = anger_coeff
            self.anxiety: uc.ParamRange = anxiety

        def __iter__(self):
            return iter(self.__dict__.items())

    def __init__(self,
                 kind_title: str,
                 maturation_days: list[int],
                 **mature_ranges: uc.RangesDict):
        self.title = kind_title
        self.maturation = tuple(
            range(i, j)
            for i, j in pairwise([0] + maturation_days)
        )
        # подсказка IDE о наличии атрибутов
        # noinspection PyTypeChecker
        self.cub: KindParameters.Ranges = None
        # noinspection PyTypeChecker
        self.young: KindParameters.Ranges = None
        # noinspection PyTypeChecker
        self.adult: KindParameters.Ranges = None
        # noinspection PyTypeChecker
        self.elder: KindParameters.Ranges = None

        for attr in list(uc.Matureness):
            setattr(self, attr, KindParameters.Ranges(
                ut.DictOfRanges(mature_ranges[attr]['health']),
                ut.DictOfRanges(mature_ranges[attr]['stamina']),
                ut.DictOfRanges(mature_ranges[attr]['hunger']),
                ut.DictOfRanges(mature_ranges[attr]['thirst']),
                ut.DictOfRanges(mature_ranges[attr]['intestine']),
                mature_ranges[attr]['activity'],
                mature_ranges[attr]['anxiety'],
                mature_ranges[attr]['anger_coeff'],
                mature_ranges[attr]['joy_coeff'],
            ))

    def age_ranges(self, days: int) -> Ranges:
        """"""
        for age, attr in zip(self.maturation, list(uc.Matureness)):
            if days in age:
                return getattr(self, attr)


@dataclass
class State:
    """

    """
    timestamp: dt
    health: float
    stamina: float
    hunger: float
    thirst: float
    intestine: float
    joy: float
    activity: float
    anger: float
    anxiety: float

    @property
    def body(self) -> dict:
        return {
            'health': self.health,
            'stamina': self.stamina,
            'hunger': self.hunger,
            'thirst': self.thirst,
            'intestine': self.intestine,
        }

    @property
    def mind(self) -> dict:
        return {
            'joy': self.joy,
            'activity': self.activity,
            'anger': self.anger,
            'anxiety': self.anxiety,
        }

    @property
    def dict(self) -> dict:
        return (
            {'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
            | self.body
            | self.mind
        )