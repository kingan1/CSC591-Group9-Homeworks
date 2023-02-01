from typing import Union, List, Dict
from options import options
from cols import Cols
from num import Num
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