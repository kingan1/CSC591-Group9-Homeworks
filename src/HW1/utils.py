import math


def rint(lo: float, hi: float):
    return math.floor(0.5 + rand(lo, hi))


class Random:
    def __init__(self):
        self.seed = 0

    def set_seed(self, value: int):
        self.seed = value

    def rand(self, lo, hi):
        """
        Generates a pseudo-random number using seed.

        :param lo: Lower limit of generated number
        :param hi: Higher limit of generated number
        :return: Pseudo-random number
        """
        lo, hi = lo or 0, hi or 1

        self.seed = (16807 * self.seed) % 2147483647
        return lo + (hi - lo) * self.seed / 2147483647


_inst = Random()
rand = _inst.rand
set_seed = _inst.set_seed


def rnd(n: float, n_places: int) -> float:
    """
    Rounds number n to n places.

    :param n: Number
    :param n_places: Number of decimal places to round
    :return: Rounded number
    """
    mult = math.pow(10, n_places or 3)
    return math.floor(n * mult + 0.5) / mult
