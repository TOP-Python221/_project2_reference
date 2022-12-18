__all__ = [
    'PersistenceManager',
]

# импорт из стандартной библиотеки
from fractions import Fraction as frac
from json import load as jload, dump as jdump, JSONDecodeError
from pprint import pprint

# импорт дополнительных модулей текущего пакета
from . import data as md
# импорт дополнительных модулей других пакетов
from ..utils import constants as uc


class JSONEmpty(Exception):
    pass

class JSONCorrupted(Exception):
    def __init__(self, file_path):
        super().__init__(f"'{file_path!s}' is corrupted")


class PersistenceManager:
    """

    """
    default_parameters_path = uc.DATA_DIR / 'production/parameters.json'
    default_states_path = uc.DATA_DIR / 'production/states.json'

    @classmethod
    def read_parameters(cls, kind: uc.Kind, parameters_path: uc.pathlike = None) -> md.KindParameters:
        """"""
        if not parameters_path:
            parameters_path = cls.default_parameters_path

        with open(parameters_path, encoding='utf-8') as filein:
            data = jload(filein)[kind.value]

        for matureness, attrs in data['ranges'].items():
            for param, infls in attrs.items():
                if not infls:
                    continue
                if isinstance(infls, str):
                    if match := uc.separated_floats_pattern.fullmatch(infls):
                        data['ranges'][matureness][param] = tuple(
                            float(n)
                            for n in infls.split(match.group('sep'))
                        )
                    else:
                        data['ranges'][matureness][param] = float(infls)
                elif isinstance(infls, dict):
                    for range, values in infls.copy().items():
                        key = tuple(int(n) for n in range.split(','))
                        val = {
                            k: float(frac(v))
                            for k, v in values.items()
                        }
                        data['ranges'][matureness][param][key] = val
                        del data['ranges'][matureness][param][range]

        return md.KindParameters(
            data['title'],
            data['maturation'],
            **data['ranges']
        )

    @classmethod
    def read_active(cls, active_path: uc.pathlike = None) -> dict:
        """"""
        if not active_path:
            active_path = cls.default_states_path
        try:
            with open(active_path, encoding='utf-8') as filein:
                data = jload(filein)
            if not data:
                raise JSONEmpty
        except (JSONEmpty, JSONDecodeError, FileNotFoundError):
            data = {}
        else:
            if set(data) != uc.ACTIVE_KEYS or set(data[uc.ACTIVE_STATE_KEY]) != uc.ACTIVE_STATE_KEYS:
                raise JSONCorrupted(active_path.name)
        return data

    @classmethod
    def write_active(cls, data: dict, active_path: uc.pathlike = None):
        """"""
        if not active_path:
            active_path = cls.default_states_path

        with open(active_path, 'w', encoding='utf-8') as fileout:
            jdump(data, fileout)


if __name__ == '__main__':
    d = PersistenceManager.read_active()
    pprint(d)

    # kr = PersistenceManager.read_parameters(uc.Kind.CAT)
    # pprint(kr.__dict__)
    # print(kr.age_ranges(42))
