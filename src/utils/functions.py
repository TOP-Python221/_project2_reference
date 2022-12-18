__all__ = [
    'countable_nouns',
]

# импорт из стандартной библиотеки
from numbers import Real

# импорт дополнительных модулей текущего пакета
from . import types as ut



def countable_nouns(number: int, nouns: tuple[str, str, str]) -> str:
    """Подставляет существительное с окончанием в зависимости от согласуемого числительного."""
    digits_nouns = (
        {1: nouns[0]}
        | dict.fromkeys((2, 3, 4), nouns[1])
        | dict.fromkeys((5, 6, 7, 8, 9, 0, 11, 12, 13, 14), nouns[2])
    )
    last_digit, two_last_digits = number % 10, number % 100
    q = digits_nouns.get(two_last_digits)
    return q if q is not None else digits_nouns[last_digit]


def uni_min(obj):
    if isinstance(obj, ut.DictOfRanges):
        return obj.min
    elif isinstance(obj, Real):
        return obj
    else:
        return min(obj)


def uni_max(obj):
    if isinstance(obj, ut.DictOfRanges):
        return obj.max
    elif isinstance(obj, Real):
        return obj
    else:
        return max(obj)


def within_range(value: Real, left: Real, right: Real) -> Real:
    if value < left:
        return left
    elif value > right:
        return right
    else:
        return value


