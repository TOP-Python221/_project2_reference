__all__ = [
    'Creature',
    'CreatureFactory'
]

# pip install schedule
# импорт сторонних пакетов
from schedule import run_pending, idle_seconds

# импорт из стандартной библиотеки
from dataclasses import dataclass
from datetime import datetime as dt
from math import floor
from pprint import pprint
from random import choice
from threading import Thread, Event
from time import sleep

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
                 joy: float,
                 activity: float,
                 anger: float,
                 anxiety: float):
        self.joy = joy
        self.activity = activity
        self.anger = anger
        self.anxiety = anxiety

    @property
    def pattern(self):
        return


class Creature:
    """

    """
    def __init__(self,
                 kind_parameters: md.KindParameters,
                 name: str,
                 birthdate: dt,
                 body: Body,
                 mind: Mind,
                 actions: uc.Actions):
        self.__kind = kind_parameters
        self.name = name
        self.birthdate = birthdate
        self.body = body
        self.mind = mind
        self._actions = actions

    @property
    def age(self) -> int:
        return (dt.now() - self.birthdate).days

    @property
    def state(self) -> md.State:
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
        # TODO: сильно тестировать необходимость применения данных формул — вместо взаимного сглаживания наблюдается взаимный разгон эмоциональных показателей
        # result['joy'] -= ranges.anger_coeff * result['anger']
        # result['anger'] -= ranges.joy_coeff * result['joy']
        if uc.DEBUG:
            print('\n...debug...')
            pprint(result)
            print('...........\n')
        return result

    def _within_range(self, attr: str, value: float):
        """"""
        attr_range = self.__kind.age_ranges(self.age)
        param = getattr(attr_range, attr)
        return uf.within_range(
            value,
            uf.uni_min(param),
            uf.uni_max(param)
        )

    def apply_tick_changes(self) -> None:
        """"""
        deltas = self._tick_changes()
        for attr in ('activity', 'anxiety'):
            new_value = self._within_range(
                attr,
                getattr(self.mind, attr) + deltas.pop(attr)
            )
            setattr(self.mind, attr, new_value)

        for attr, coeff in (('joy', 'activity'), ('anger', 'anxiety')):
            new_value = self._within_range(
                attr,
                getattr(self.mind, attr) + getattr(self.mind, coeff) * deltas.pop(attr)
            )
            setattr(self.mind, attr, new_value)

        for attr, delta in deltas.items():
            new_value = self._within_range(
                attr,
                getattr(self.body, attr) + delta
            )
            setattr(self.body, attr, new_value)

        if uc.DEBUG:
            print('\n...debug...')
            pprint(self.state.dict)
            print('...........\n')

    @staticmethod
    def continuous_tick(event_obj: Event, interval: float = 1) -> Thread:
        """"""

        class BackgroundCycleThread(Thread):
            @classmethod
            def run(cls) -> None:
                while not event_obj.is_set():
                    run_pending()
                    # if uc.DEBUG:
                    #     print(f'\n...до следующего обновления параметров {idle_seconds():.2} секунд...\n')
                    sleep(interval)

        thread_obj = BackgroundCycleThread()
        thread_obj.start()
        return thread_obj

    def __str__(self):
        age = self.age
        noun = uf.countable_nouns(age, ('день', 'дня', 'дней'))
        return (
            f"{self.name}: {age} {noun}"
        )

    def feed(self):
        """"""

    def clean(self):
        """"""

    def play(self):
        """"""

    def talk(self):
        """"""

    def action(self):
        """"""
        random_action = choice(self._actions)
        random_action(self)


class CreatureActions(Creature):
    """

    """
    def run_at_night(self):
        """"""
        self.mind.joy = self._within_range('joy', self.mind.joy + 30)
        print('Ночной тыгыдык!')

    def seek_for_honey(self):
        """"""

    def get_warm_on_sun(self):
        """"""

    kind_actions = {
        uc.Kind.CAT: (run_at_night, ),
        uc.Kind.DOG: (),
        uc.Kind.BEAR: (seek_for_honey, ),
        uc.Kind.LIZARD: (get_warm_on_sun, ),
        uc.Kind.SNAKE: (get_warm_on_sun, ),
    }


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
        loaded['last_state']['timestamp'] = dt.strptime(
            loaded['last_state']['timestamp'],
            '%Y-%m-%d %H:%M:%S'
        )
        self.last_state = md.State(**loaded['last_state'])

    def revive_creature(self) -> Creature:
        """"""
        pet = Creature(
            self.__parameters,
            self.name,
            self.birthdate,
            Body(**self.last_state.body),
            Mind(**self.last_state.mind),
            CreatureActions.kind_actions[self.kind],
        )
        hours = (dt.now() - self.last_state.timestamp).seconds // 3600
        for _ in range(hours):
            if choice((True, False)):
                # случайное действие
                pass
            pet.apply_tick_changes()
        return pet

    def new_creature(self) -> Creature:
        """"""
        return Creature(
            self.__parameters,
            self.name,
            dt.now(),
            Body(
                health=floor(self.__parameters.cub.health.max / 3),
                stamina=floor(self.__parameters.cub.stamina.max / 5),
                hunger=floor(self.__parameters.cub.hunger.max),
                thirst=floor(self.__parameters.cub.thirst.max / 1.5),
                intestine=0,
            ),
            Mind(
                joy=0,
                activity=min(self.__parameters.cub.activity),
                anger=floor(max(self.__parameters.cub.anger) / 4),
                anxiety=max(self.__parameters.cub.anxiety),
            ),
            CreatureActions.kind_actions[self.kind],
        )
