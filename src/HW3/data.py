import math
from typing import Union, List, Dict

from cols import Cols
from num import Num
from options import options
from row import Row
from sym import Sym
from utils import csv


class Data:
    def __init__(self, src: Union[str, List]) -> None:
        self.rows = list()
        self.cols = None

        if type(src) == str:
            csv(src, self.add)
        else:
            map(self.add, src or [])

    def add(self, t: Union[List, Row]):
        """
        Adds a new row and updates column headers.

        :param t: Row to be added
        """
        if self.cols:
            t = t if isinstance(t, Row) else Row(t)

            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = Cols(t)

    def clone(self, init: List) -> 'Data':
        """
        Returns a clone with the same structure as self.

        :param init: Initial data for the clone
        """
        data = Data(list(self.cols.names))
        map(self.add, init or [])

        return data

    def stats(self, cols: List[Union[Sym, Num]], nplaces: int, what: str = "mid") -> Dict:
        """
        Returns mid or div of cols (defaults to i.cols.y).

        :param cols: Columns to collect statistics for
        :param nplaces: Decimal places to round the statistics
        :param what: Statistics to collect
        :return: Dict with all statistics for the columns
        """
        return dict(sorted({col.txt: col.rnd(getattr(col, what)(), nplaces) for col in cols or self.cols.y}.items()))

    def cluster(self, rows=None, min_=None, cols=None, above=None):
        """
        Performs N-level bi clustering on the rows.

        :param rows: Data points to cluster
        :param min_: Clustering threshold value
        :param cols: Columns to cluster on
        :param above: Point chosen as A
        :return: Rows under the current node
        """
        rows = self.rows if rows is None else rows
        cols = self.cols if cols is None else cols

        min_ = len(rows) ** options["min"] if min_ is None else min_

        node = self.clone(rows)

        if len(rows) > 2 * min_:
            left, right, node.A, node.B, node.mid = self.half(rows, cols, above)

            node.left = self.cluster(left, min_, cols, node.A)
            node.right = self.cluster(right, min_, cols, node.B)

        return node

    def sway(self, rows=None, min=0, cols=None, above=None):
        """
            Returns best half, recursively
        """
        rows = rows or self.rows
        min = min or len(rows) ** options['min']
        cols = cols or self.cols.x
        node = {"data": self.clone(rows)}

        if len(rows) > 2 * min:
            left, right, node['A'], node['B'], node['mid'], _ = self.half(rows, cols, above)
            if self.better(node['B'], node['A']):
                left, right, node['A'], node['B'] = right, left, node['B'], node['A']
            node['left'] = self.sway(left, min, cols, node['A'])
        return node

    def better(self, row1, row2):
        s1 = 0
        s2 = 0
        ys = self.cols.y
        for _, col in enumerate(ys):
            x = Num.norm(row1.cells[col.at])
            y = Num.norm(row2.cells[col.at])
            s1 = s1 - math.exp(col.w * (x - y) / len(ys))
            s2 = s2 - math.exp(col.w * (y - x) / len(ys))
        return s1 / len(ys) < s2 / len(ys)
