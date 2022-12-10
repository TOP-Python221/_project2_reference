__all__ = [
    'DictOfRanges'
]


class DictOfRanges(dict):
    """

    """
    def __getitem__(self, item):
        if isinstance(item, int):
            for left, right in self:
                if left <= item <= right or right <= item <= left:
                    return super().__getitem__((left, right))
            raise KeyError(f"{item} doesn't refer to any range in dict")
        else:
            return super().__getitem__(item)

    @property
    def min(self):
        return min([n for key in self for n in key])

    @property
    def max(self):
        return max([n for key in self for n in key])


class DictSummingValues(dict):
    """

    """
    def __add(self, other, err_msg: str):
        if isinstance(other, dict):
            result = DictSummingValues()
            for key in set(self) - set(other):
                result[key] = self[key]
            for key in set(self) & set(other):
                result[key] = self[key] + other[key]
            for key in set(other) - set(self):
                result[key] = other[key]
            return result
        else:
            raise TypeError(err_msg)

    def __add__(self, other):
        return self.__add(other, f"unsupported operand type(s) for +: 'dict' and '{type(other).__name__}'")

    def __radd__(self, other):
        return self.__add(other, f"unsupported operand type(s) for +: '{type(other).__name__}' and 'dict'")

    def __iadd__(self, other):
        if isinstance(other, dict):
            for key in set(self) & set(other):
                self[key] += other[key]
            for key in set(other) - set(self):
                self[key] = other[key]
            return self
        else:
            raise TypeError(f"unsupported operand type(s) for +=: 'dict' and '{type(other).__name__}'")


if __name__ == '__main__':
    d1 = DictSummingValues({'a': 1, 'b': 2, 'c': 3})
    d2 = d1 + {'a': 10}
    d3 = {'b': 12} + d1
    print(d2.__class__)
    print(d2)
    print(d3.__class__)
    print(d3)
    # d4 = [1, 2, 3] + d2
    d5 = DictSummingValues()
    d5 += {'x': 3, 'y': 2}
    print(d5.__class__)
    print(d5)

