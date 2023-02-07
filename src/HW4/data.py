import math
from typing import Union, List, Dict

from cols import Cols
from num import Num
from options import options
from row import Row
from sym import Sym
from utils import csv, many, cosine, any, copy, helper


class Data:
    def __init__(self, src: Union[str, List]) -> None:
        self.rows = list()
        self.cols = None
        if type(src) == str:
            csv(src, self.add)
        else:
            self.add(src or [])

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
        list(map(data.add, init or []))

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

    def cluster(self, rows: List[Row] = None, min_: int = None, cols: List[Union[Sym, Num]] = None, above: Row = None):
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

        min_ = len(rows) ** options["min"] if min_ is None else min_

        node = {"data": self.clone(rows)}

        if len(rows) > 2 * min_:
            left, right, node['A'], node['B'], node['mid'],_ = self.half(rows, cols, above)

            node['left'] = self.cluster(left, min_, cols, node['A'])
            node['right'] = self.cluster(right, min_, cols, node['B'])

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
            x = col.norm(row1.cells[col.at])
            y = col.norm(row2.cells[col.at])
            s1 = s1 - math.exp(col.w * (x - y) / len(ys))
            s2 = s2 - math.exp(col.w * (y - x) / len(ys))
        return s1 / len(ys) < s2 / len(ys)
 
    def dist(self,row1,row2,cols=None):
        n = 0
        dis = 0
        cols = (cols if cols else self.cols.x)
        for _,c in enumerate(cols):
            n = n + 1
            dis = dis + c.dist(row1.cells[c.at], row2.cells[c.at]) ** options['p']
        return (dis/n) ** (1/options['p'])
    
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
        def dist(row1, row2):
            return self.dist(row1, row2, cols)

        def project(row):
            return {"row": row, "dist": cosine(dist(row, A), dist(row, B), c)}
        
        left , right = [],[]
        rows = (rows if rows else self.rows)
        some = many(rows, options["Sample"], options['seed'])     
        A = any(some,above if above else options['seed'])
        B = self.around(A, some)[int(options["Far"] * len(rows)) // 1]["row"]
        c = dist(A,B)

        for n, tmp in enumerate(sorted(list(map(project, rows)), key=lambda x: x["dist"])):
            if n <= len(rows) // 2:
                left.append(tmp["row"])
                mid = tmp["row"]
            else:
                right.append(tmp["row"])

        return left, right, A, B, mid, c


def rep_rows(t, rows):
    rows = copy(rows)

    for j, s in rows[-1]:
        rows[1][j] += (":" + s)

    del rows[-1]

    for n, row in enumerate(rows):
        if n == 1:
            row.append("thingX")
        else:
            u = t.rows[-(n - 1)]
            row.append(u[-1])

    return Data(rows)


def rep_cols(cols):
    cols = copy(cols)

    for column in cols:
        column[len(column)-1] = str(column[0]) + ':' + str(column[len(column)-1])

        for j in range(1, len(column)):
            column[j-1] = column[j]

        column.pop()

    cols.insert(0, [helper(i) for i in range(len(cols[0])-1)])
    cols[0][len(cols[0])-1] = "thingX"

    return Data(cols)
