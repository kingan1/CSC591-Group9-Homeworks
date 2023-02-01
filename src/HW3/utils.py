import io
import math
import re


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


def coerce(v):
    """
    Attempts to convert v to an int, float, bool, or keep as string

    :param v: String to convert
    :return: v converted to its type
    """
    types = [int, float]

    for t in types:
        try:
            return t(v)
        except ValueError:
            pass

    bool_vals = ["true", "false"]
    if v.lower() in bool_vals:
        return v.lower() == "true"

    return v


def csv(sFilename, fun):
    """
        call `fun` on rows (after coercing cell text)

        :param sFilename: String of the file to read
        :param fun: function to call per each row

    """
    f = io.open(sFilename)
    while True:
        s = f.readline().rstrip()
        if s:
            t = []
            for s1 in re.findall("([^,]+)", s):
                t.append(coerce(s1))
            fun(t)
        else:
            return f.close()

def cosine(a, b, c):
    """
        find x, y from a line connecting 'a' to 'b'
    """
    # might be an issue if c is 0
    if c == 0:
        return 0
    x1 = (a**2 + c**2 - b**2) / (2*c)
    x2 = max(0, min(1, x1))
    #  -- in the incremental case, x1 might be outside 0,1
    y  = (a**2 - x2**2)**.5
    return x2, y