__all__ = [
    'Creature',
    'CreatureFactory'
]

# импорт из стандартной библиотеки
from abc import ABC
from dataclasses import dataclass
from datetime import datetime as dt
from math import floor
from pprint import pprint

# импорт дополнительных модулей текущего пакета
import model.data as md
import model.files_io as fio
# импорт дополнительных модулей других пакетов
import utils.constants as uc
import utils.functions as uf
import utils.types as ut


@dataclass
class Body:
    """

    """
    health: float
    stamina: float
    hunger: float
    thirst: float
    intestine: float


class Mind:
    """

    """
    patterns: ut.DictOfRanges

    def __init__(self,
                 joy: int,
                 activity: float,
                 anger: int,
                 anxiety: float):
        self.joy = joy
        self.activity = activity
        self.anger = anger
        self.anxiety = anxiety

    @property
    def pattern(self):
        return


class Creature(ABC):
    """

    """

    def __init__(self,
                 kind_parameters: md.KindParameters,
                 name: str,
                 birthdate: dt,
                 body: Body,
                 mind: Mind):
        self.__kind = kind_parameters
        self.name = name
        self.birthdate = birthdate
        self.body = body
        self.mind = mind

    @property
    def age(self) -> int:
        return (dt.now() - self.birthdate).days

    @property
    def state(self):
        return md.State(
            timestamp=dt.now(),
            **self.body.__dict__,
            **self.mind.__dict__,
        )

    def _tick_changes(self) -> dict:
        """"""
        result = ut.DictSummingValues()
        ranges = self.__kind.age_ranges(self.age)
        for param, value in self.body.__dict__.items():
            result += getattr(ranges, param)[value]
        # сильно тестировать необходимость применения данных формул — вместо взаимного сглаживания наблюдается взаимный разгон эмоциональных показателей
        # result['joy'] -= ranges.anger_coeff * result['anger']
        # result['anger'] -= ranges.joy_coeff * result['joy']
        return result

    def apply_tick_changes(self):
        """"""
        ranges = self.__kind.age_ranges(self.age)
        deltas = self._tick_changes()
        for attr in ('activity', 'anxiety'):
            new_value = getattr(self.mind, attr) + deltas.pop(attr)
            if new_value < (range_min := uf.uni_min(getattr(ranges, attr))):
                new_value = range_min
            elif new_value > (range_max := uf.uni_max(getattr(ranges, attr))):
                new_value = range_max
            setattr(self.mind, attr, new_value)

        for attr, coeff in (('joy', 'activity'), ('anger', 'anxiety')):
            new_value = getattr(self.mind, attr) + getattr(self.mind, coeff) * deltas.pop(attr)
            if new_value < (range_min := uf.uni_min(getattr(ranges, attr))):
                new_value = range_min
            elif new_value > (range_max := uf.uni_max(getattr(ranges, attr))):
                new_value = range_max
            setattr(self.mind, attr, new_value)

        for attr, delta in deltas.items():
            # if attr in dir(self.body):
            new_value = getattr(self.body, attr) + delta
            range_min = uf.uni_min(getattr(ranges, attr))
            if new_value < range_min:
                new_value = range_min
            range_max = uf.uni_max(getattr(ranges, attr))
            if new_value > range_max:
                new_value = range_max
            setattr(self.body, attr, new_value)

        pprint(self.state)

    def __str__(self):
        age = self.age
        noun = uf.countable_nouns(age, ('день', 'дня', 'дней'))
        return (
            f"{self.name}: {age} {noun}"
        )


class CreatureActions(Creature):
    """

    """

    def run_at_night(self):
        """"""

    def seek_for_honey(self):
        """"""

    def get_warm_on_sun(self):
        """"""


class CreatureFactory:
    """

    """

    # noinspection PyTypeChecker
    def __init__(self):
        self.__parameters: md.KindParameters = None
        self.name: str = None
        self.birthdate: dt = None
        self.last_state: md.State = None

    def __bool__(self):
        return all(map(bool, self.__dict__.values()))

    @property
    def kind(self):
        return uc.Kind(self.__parameters.title)

    @kind.setter
    def kind(self, kind_: uc.Kind):
        self.__parameters = fio.PersistenceManager.read_parameters(kind_)

    @property
    def creature_data(self) -> dict:
        return {
            'kind': self.kind.value,
            'name': self.name,
            'birthdate': self.birthdate.strftime('%Y-%m-%d %H:%M:%S'),
            'last_state': self.last_state.dict,
        }

    @creature_data.setter
    def creature_data(self, loaded: dict):
        self.kind = uc.Kind(loaded['kind'])
        self.name = loaded['name']
        self.birthdate = dt.strptime(loaded['birthdate'], '%Y-%m-%d %H:%M:%S')
        loaded['last_state']['timestamp'] = dt.strptime(loaded['last_state']['timestamp'], '%Y-%m-%d %H:%M:%S')
        self.last_state = md.State(**loaded['last_state'])

    def _revive_body(self) -> Body:
        """"""

    def _revive_mind(self) -> Mind:
        """"""

    def revive_creature(self) -> Creature:
        """"""
        return Creature(
            self.__parameters,
            self.name,
            self.birthdate,
            self._revive_body(),
            self._revive_mind()
        )

    def _new_body(self) -> Body:
        """"""
        return Body(
            health=floor(self.__parameters.cub.health.max / 3),
            stamina=floor(self.__parameters.cub.stamina.max / 5),
            hunger=floor(self.__parameters.cub.hunger.max),
            thirst=floor(self.__parameters.cub.thirst.max / 1.5),
            intestine=0,
        )

    def _new_mind(self) -> Mind:
        """"""
        return Mind(
            joy=0,
            activity=min(self.__parameters.cub.activity),
            anger=floor(max(self.__parameters.cub.anger) / 4),
            anxiety=max(self.__parameters.cub.anxiety),
        )

    def new_creature(self) -> Creature:
        """"""
        return Creature(
            self.__parameters,
            self.name,
            dt.now(),
            self._new_body(),
            self._new_mind()
        )
