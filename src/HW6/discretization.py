from math import inf, floor
from typing import Union, Optional, List, Dict

from num import Num
from options import options
from row import Row
from sym import Sym
from utils import copy


class Range:
    def __init__(self, at, txt, lo, hi=None):
        self.at = at
        self.txt = txt

        self.lo = lo
        self.hi = lo or hi or lo

        self.y = Sym()

    def extend(self, n: int, s: str):
        self.lo = min(n, self.lo)
        self.hi = max(n, self.hi)

        self.y.add(s)


def merge(col1: Union[Sym, Num], col2: Union[Sym, Num]) -> Union[Sym, Num]:
    new = copy(col1)

    if isinstance(col1, Sym):
        for x, n in col2.has.items():
            new.add(x, n)
    else:
        for _, n in col2.has.items():
            new.add(n)

        new.lo = min(col1.lo, col2.lo)
        new.hi = max(col1.hi, col2.hi)

    return new


def merge2(col1: Union[Sym, Num], col2: Union[Sym, Num]) -> Optional[Union[Sym, Num]]:
    new = merge(col1, col2)

    if new.div() <= ((col1.div() * col1.n) + (col2.div() * col2.n)) / new.n:
        return new


def merge_any(ranges0: List[Range]) -> List[Range]:
    def no_gaps(t: List[Range]):
        if not t:
            return t

        for j in range(1, len(t)):
            t[j].lo = t[j - 1].hi

        t[0].lo = -inf
        t[len(t) - 1].hi = inf

        return t

    ranges1 = []
    j = 0

    while j < len(ranges0):
        left = ranges0[j]
        right = None if j == len(ranges0) - 1 else ranges0[j + 1]

        if right is not None:
            y = merge2(left.y, right.y)

            if y is not None:
                j += 1
                left.hi, left.y = right.hi, y

        ranges1.append(left)
        j += 1
    return no_gaps(ranges0) if len(ranges0) == len(ranges1) else merge_any(ranges1)


def bin(col: Union[Sym, Num], x):
    if x == "?" or isinstance(col, Sym):
        return x

    tmp = (col.hi - col.lo) / (options["bins"] - 1)

    return 1 if col.hi == col.lo else floor(x / tmp + 0.5) * tmp


def extend(range, n, s):
    range.lo = min(n, range.lo)
    range.hi = max(n, range.hi)
    range.y.add(s)


def bins(cols: List[Union[Sym, Num]], rowss: Dict[str, List[Row]]):
    out = []

    for col in cols:
        ranges_dict = {}

        for y, rows in rowss.items():
            for row in rows:
                x = row.cells[col.at]

                if x != "?":
                    k = bin(col, x)

                    ranges_dict[k] = ranges_dict.get(k, Range(col.at, col.txt, x))
                    extend(ranges_dict[k], x, y)

        ranges_dict = (sorted(ranges_dict.items(), key=lambda x: x[1].lo))
        ranges = [r[1] for r in ranges_dict]
        out.append(ranges if isinstance(col, Sym) else merge_any(ranges))

    return out


def value(has, n_b: int = 1, n_r: int = 1, s_goal: str = None) -> float:
    b, r = 0, 0

    for x, n in has.items():
        if x == s_goal:
            b = b + n
        else:
            r = r + n

    b, r = b / (n_b + 1 / inf), r / (n_r + 1 / inf)
    return b ** 2 / (b + r)
