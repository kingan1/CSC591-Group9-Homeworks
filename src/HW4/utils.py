import copy as cp
import io
import math
import random
import re
from typing import List, Union


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

    if type(y) == complex:
        y = y.real
    return x2, y


def show(node, what: str = "mid", cols: List[Union['Sym', 'Num']] = None, nplaces: int = 2, lvl: int = 0) -> None:
    """
    Prints the tree.

    :param node: Node of tree
    :param what: Statistics to print
    :param cols: Columns to print stats for
    :param nplaces: Number of decimals to round the values to
    :param lvl: Level in the tree
    """
    if node:
        print(
            f"{'| ' * lvl}"
            f"{len(node['data'].rows)}  "
            f"{node['data'].stats(node['data'].cols.y, nplaces, 'mid') if 'left' not in node or lvl == 0 else ''}"
        )

        show(node.get('left', None), what, cols, nplaces, lvl + 1)
        show(node.get('right', None), what, cols, nplaces, lvl + 1)

def many(t, n, seed= 937162211):
    """
    returns some items from `t`
    """
    random.seed(seed)
    return random.choices(t, k=n)

def any(t, seed=937162211):
    """
    returns one items at random
    """
    random.seed(seed)
    return random.choices(t)[0]
def helper(k):
    return "Num" + str(k)

def repCols(cols, Data):
    cols = copy(cols)
    for column in cols:
        column[len(column)-1] = str(column[0]) + ':' + str(column[len(column)-1])
        for j in range(1,len(column)):
            column[j-1] = column[j]
    column.pop()
    cols.insert(0,[helper(i) for i in range(len(cols[0])-1)])
    cols[0][len(cols[0])-1] = "thingX"
    return Data(cols)


def copy(t):
    return cp.deepcopy(t)


def do_file(file):
    return exec(open(file).read())
