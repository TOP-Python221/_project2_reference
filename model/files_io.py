__all__ = [
    'PersistenceManager',
]

# импорт из стандартной библиотеки
from fractions import Fraction as frac
from json import load as jload, dump as jdump, JSONDecodeError
from pprint import pprint

# импорт дополнительных модулей текущего пакета
import model.data as md
# импорт дополнительных модулей других пакетов
import utils.constants as uc


class PersistenceManager:
    """

    """
    default_parameters_path = uc.BASE_DIR / 'model/parameters.json'
    default_states_path = uc.BASE_DIR / 'model/states.json'

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
    def read_states(cls, states_path: uc.pathlike = None) -> dict:
        """"""
        if not states_path:
            states_path = cls.default_states_path
        try:
            with open(states_path, encoding='utf-8') as filein:
                data = jload(filein)
        except JSONDecodeError:
            data = {}
        except FileNotFoundError:
            data = {}
        return data

    @classmethod
    def write_states(cls, data: dict, states_path: uc.pathlike = None):
        """"""
        if not states_path:
            states_path = cls.default_states_path

        with open(states_path, 'w', encoding='utf-8') as fileout:
            jdump(data, fileout)


if __name__ == '__main__':
    d = PersistenceManager.read_states()
    pprint(d)

    # kr = PersistenceManager.read_parameters(uc.Kind.CAT)
    # pprint(kr.__dict__)
    # print(kr.age_ranges(42))
