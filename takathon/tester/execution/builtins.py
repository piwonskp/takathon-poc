import random
import sys

from unittest.mock import Mock


def any_of(*choices):
    return random.choice(choices)


def interval(lower, upper):
    is_float = type(lower) == float or type(upper) == float
    if is_float:
        random.uniform(float(lower), float(upper))

    return random.randint(int(lower), int(upper))


class Infinity:
    def __init__(self, negative=False):
        self.negative = negative

    def __neg__(self):
        return Infinity(negative=True)

    def sign(self, val):
        return -val if self.negative else val

    def __int__(self):
        return self.sign(sys.maxsize)

    def __float__(self):
        return self.sign(float(sys.maxsize))


def between(lower, upper):
    return lambda result: lower < result < upper


BUILTINS = {
    'Mock': Mock,
    'any_of': any_of,
    'interval': interval,
    'Infinity': Infinity(),
    'between': between
}
