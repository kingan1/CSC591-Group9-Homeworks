import collections
import math
from typing import Union


class Sym:
    """
    Summarizes a stream of Symbols.
    """

    def __init__(self, at: int = 0, txt: str = ""):
        self.at = at
        self.txt = txt

        self.n = 0
        self.has = collections.defaultdict(int)
        self.most = 0
        self.mode = None

    def add(self, x: str):
        """
        Updates counts of things seen so far

        :param x: Symbol to add
        """
        if x != "?":
            self.n = self.n + 1
            self.has[x] = 1 + (self.has[x] or 0)
            if self.has[x] > self.most:
                self.most = self.has[x]
                self.mode = x
        return x

    def mid(self):
        """
        Returns the mode
        """
        return self.mode

    def div(self):
        """
        Returns the entropy
        """

        def fun(p):
            return p * math.log(p, 2)

        e = 0

        for _, n in self.has.items():
            e = e + fun(n / self.n)
        return -e

    @staticmethod
    def rnd(x: Union[float, str], n: int) -> Union[float, str]:
        """
        Returns a rounded number : SYM's do not get rounded
        :param x: Number to round
        :param n: Number of decimal places to round
        :return: x
        """
        return x
