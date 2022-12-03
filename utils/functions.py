__all__ = [
    'countable_nouns',
]


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


