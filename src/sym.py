import math


class Sym:
    """
    Summarizes a stream of Symbols.
    """

    def __init__(self):
        self.n = 0
        self.has = {}
        self.most = 0
        self.mode = None

    def add(self, x: str):
        """
        Updates counts of things seen so far

        :param x: Symbol to add
        """

        if x != "?":
            self.n = self.n + 1
            self.has[x] = 1 + (self.has.get(x, 0))
            if self.has[x] > self.most:
                self.most = self.has[x]
                self.mode = x

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
