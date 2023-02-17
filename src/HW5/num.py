import math
from typing import Union
from options import options
from utils import rnd, rand, rint


class Num:
    """
    Summarizes a stream of numbers.
    """

    def __init__(self, at: int = 0, txt: str = ""):
        self.at = at
        self.txt = txt

        self.n = 0

        self.lo = math.inf
        self.hi = -math.inf
        self.ok = True
        self.has_ = {}

        self.w = -1 if self.txt.endswith("-") else 1

    def add(self, x, n: float=1) -> None:
        """
        Adds n and updates lo, hi and stuff needed for standard deviation.

        :param n: Number to add
        :return: None
        """
        if x != "?":
            self.n += n

            self.lo, self.hi = min(x,self.lo), max(x,self.hi) 
            
            all = len(self.has_)

            pos = all+1 if all < options['Max'] else rint(1, all) if rand() < options['Max']/self.n else 0
            
            if pos:
                self.has_[pos] = x
                self.ok = False


    def mid(self) -> float:
        """
        Returns mean of the numbers added to the stream.

        :return: Mean of the numbers
        """
        return per(self.has(), .5)

    def div(self) -> float:
        """
        Returns standard deviation of the numbers using Welford's algorithm.

        :return: Standard deviation of the numbers
        """
        return 0 if (self.m2 < 0 or self.n < 2) else math.pow((self.m2 / (self.n - 1)), 0.5)

    @staticmethod
    def rnd(x: Union[float, str], n: int) -> Union[float, str]:
        """
        Returns a rounded number

        :param x: Number to round
        :param n: Number of decimal places to round
        :return: Rounded number
        """
        return x if x == "?" else rnd(x, n)

    def dist(self, n1, n2):
        if n1 == '?' and n2 == '?':
            return 1
        n1 = self.norm(n1)
        n2 = self.norm(n2)
        if n1 == "?":
            if n2 < 0.5:
                n1 = 1
            else:
                n1 = 0
        if n2 == "?":
            if n1 < 0.5:
                n2 = 1
            else:
                n2 = 0
        return abs(n1 - n2)

    def norm(self, num):
        if num == "?":
            return num
        return (num - self.lo) / (self.hi - self.lo + 1e-32)
    
    def has(self):
        ret = dict(sorted(self.has_.items(), key=lambda x: x[1]))
        self.ok = True
        return list(ret.values())
