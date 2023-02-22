import math
from typing import Union, List, Dict

from cols import Cols
from num import Num
from options import options
from row import Row
from sym import Sym

from utils import *


class Data:

    def __init__(self):
        self.rows = list()
        self.cols = None

    def read(self, src: Union[str, List]) -> None:
        def f(t):
            self.add(t)

        csv(src, f)

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

    @staticmethod
    def clone(data, ts={}) -> 'Data':
        """
        Returns a clone with the same structure as self.

        :param init: Initial data for the clone
        """
        data1 = Data()
        data1.add(data.cols.names)
        for _, t in enumerate(ts or {}):
            data1.add(t)
        return data1

    def stats(self, cols: List[Union[Sym, Num]] = None, nplaces: int = 2, what: str = "mid") -> Dict:
        """
        Returns mid or div of cols (defaults to i.cols.y).

        :param cols: Columns to collect statistics for
        :param nplaces: Decimal places to round the statistics
        :param what: Statistics to collect
        :return: Dict with all statistics for the columns
        """
        ret = dict(sorted({col.txt: rnd(getattr(col, what)(), nplaces) for col in cols or self.cols.y}.items()))
        ret["N"] = len(self.rows)
        return ret

    def cluster(self, rows: List[Row] = None, cols: List[Union[Sym, Num]] = None, above: Row = None):
        """
        Performs N-level bi clustering on the rows.

        :param rows: Data points to cluster
        :param min_: Clustering threshold value
        :param cols: Columns to cluster on
        :param above: Point chosen as A
        :return: Rows under the current node
        """
        rows = self.rows if rows is None else rows
        cols = self.cols.x if cols is None else cols

        node = {"data": self.clone(rows)}

        if len(rows) >= 2:
            left, right, node['A'], node['B'], node['mid'], node['c'] = self.half(rows, cols, above)

            node['left'] = self.cluster(left, cols, node['A'])
            node['right'] = self.cluster(right, cols, node['B'])

        return node

    def sway(self, cols=None):

        def worker(rows, worse, above=None):
            if len(rows) <= len(self.rows) ** options["min"]:
                return rows, many(worse, options['rest'] * len(rows))
            l, r, A, B, c = self.half(rows, cols, above)
            if self.better(B, A):
                l, r, A, B = r, l, B, A
            for x in r:
                worse.append(x)

            return worker(l, worse, A)

        best, rest = worker(self.rows, [])

        return Data.clone(self, best), Data.clone(self, rest)

    def better(self, row1, row2, s1=0, s2=0, ys=None, x=0, y=0):
        if not ys:
            ys = self.cols.y
        for col in ys:
            x = norm(col, row1.cells[col.at])
            y = norm(col, row2.cells[col.at])
            s1 = s1 - math.exp(col.w * (x - y) / len(ys))
            s2 = s2 - math.exp(col.w * (y - x) / len(ys))
        return s1 / len(ys) < s2 / len(ys)

    def around(self, row1, rows=None, cols=None):
        """
        sort other `rows` by distance to `row`
        """
        rows = (rows if rows else self.rows)
        cols = (cols if cols else self.cols.x)

        def func(row2):
            return {'row': row2, 'dist': self.dist(row1, row2, cols)}

        return sorted(list(map(func, rows)), key=lambda x: x['dist'])

    def half(self, rows=None, cols=None, above=None):
        """
        divides data using 2 far points
        """

        def gap(r1, r2):
            return dist(self, r1, r2, cols)

        def cos(a, b, c):
            return (a ** 2 + c ** 2 - b ** 2) / (2 * c)

        def proj(r):
            return {'row': r, 'x': cos(gap(r, A), gap(r, B), c)}

        rows = rows or self.rows
        some = many(rows, options["Halves"])
        A = above if above else any(some)
        tmp = sorted([{"row": r, "d": gap(r, A)} for r in some], key=lambda x: x["d"])
        far = tmp[int((len(tmp)-1) * options["Far"])]
        B, c = far["row"], far["d"]
        sorted_rows = sorted(map(proj, rows), key=lambda x: x["x"])
        left, right = [], []
        for n, two in enumerate(sorted_rows):
            if (n+1) <= (len(rows) / 2):
                left.append(two["row"])
            else:
                right.append(two["row"])
        return left, right, A, B, c

    def tree(self, rows=None, cols=None, above=None):
        rows = rows if rows else self.rows

        here = {"data": Data.clone(self, rows)}

        if (len(rows)) >= 2 * ((len(self.rows)) ** options['min']):
            left, right, A, B, _ = self.half(rows, cols, above)
            here["left"] = self.tree(left, cols, A)
            here["right"] = self.tree(right, cols, B)
        return here

def rep_rows(t, rows):
    rows = copy(rows)
    for j, s in enumerate(rows[-1]):
        rows[0][j] += (":" + s)

    del rows[-1]

    for n, row in enumerate(rows):
        if n == 0:
            row.append("thingX")
        else:
            u = t['rows'][len(t['rows']) - n]
            row.append(u[-1])
    return Data(rows)


def rep_cols(cols):
    cols = copy(cols)

    for column in cols:
        column[len(column) - 1] = str(column[0]) + ':' + str(column[len(column) - 1])

        for j in range(1, len(column)):
            column[j - 1] = column[j]

        column.pop()

    cols.insert(0, [helper(i + 1) for i in range(len(cols[0]))])
    cols[0][len(cols[0]) - 1] = "thingX"
    return Data(cols)


def rep_place(data):
    n = 20
    g = [[''] * n for _ in range(n)]
    maxy = 0
    print("")
    for r, row in enumerate(data.rows):
        c = chr(64 + r + 1)
        print(c, row.cells[-1])
        x, y = int(row.x * n), int(row.y * n)
        maxy = max(maxy, y)
        g[y][x] = c
    print("")
    for y in range(0, maxy):
        frmt = "{:>3}" * len(g[y])

        print("{" + frmt.format(*g[y]) + "}")


def rep_grid(sFile):
    t = do_file(sFile)
    rows = rep_rows(t, transpose(t['cols']))
    cols = rep_cols(t['cols'])
    show(rows.cluster())
    show(cols.cluster())
    rep_place(rows)
