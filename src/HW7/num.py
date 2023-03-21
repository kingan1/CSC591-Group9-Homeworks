
from utils import per


class Num:
    """
    Summarizes a stream of numbers.
    """

    def __init__(self, t=[]):
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.sd = 0
        for x in t:
            self.add(x)

    def add(self, x) -> None:
        """
        Adds n and updates lo, hi and stuff needed for standard deviation.

        :param n: Number to add
        :return: None
        """
        self.n += 1
        d = x - self.mu
        self.mu = self.mu + d/self.n
        self.m2 = self.m2 + d*(x-self.mu)
        self.sd = 0 if self.n<2 else (self.m2/(self.n - 1))**.5

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
        return (per(self.has(), .9) - per(self.has(), .1)) / 2.58

    def has(self):
        ret = dict(sorted(self.has_.items(), key=lambda x: x[1]))
        self.ok = True
        return list(ret.values())
