from math import inf
from typing import Union, Optional, List

from num import Num
from sym import Sym
from utils import copy


class Range:
    def __init__(self, at, txt, lo, hi):
        self.at = at
        self.txt = txt

        self.lo = lo
        self.hi = hi

        self.y = Sym()

    def extend(self, n, s):
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
        for j in range(2, len(t)):
            t[j].lo = t[j - 1].hi

        t[1].lo = -inf
        t[len(t)].hi = inf

    ranges1 = []
    j = 1

    while j <= len(ranges0):
        left, right = ranges0[j], ranges0[j + 1]

        if right is not None:
            y = merge2(left.y, right.y)

            if y is not None:
                j += 1
                left.hi, left.y = right.hi, y

        ranges1.append(left)
        j += 1

    return no_gaps(ranges0) if len(ranges0) == len(ranges1) else merge_any(ranges1)
