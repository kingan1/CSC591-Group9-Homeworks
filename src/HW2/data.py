from cols import Cols
from row import Row
from utils import kap, map, csv


class Data:
    def __init__(self, src) -> None:
        self.rows = list()
        self.cols = None
        if type(src) == str:
            csv(src, self.add)
        else:
            map(src or {}, self.add)

    def add(self, t):
        if self.cols:
            t = t.cells and t or Row(t)
            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = Cols(t)

    def clone(self, init):
        data = Data(list(self.cols.names))
        map(init or [], self.add)
        return data

    def stats(self, cols, nplaces, what="mid"):
        def fun(k, col):
            return col.rnd((col, what)(), nplaces), col.txt

        return kap(fun, cols or self.cols.y)
