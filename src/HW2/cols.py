import re

from num import Num
from row import Row
from sym import Sym


class Cols:
    """
    Factory for managing a set of NUMs or SYMs
    """
    def __init__(self, t):
        self.names, self.all, self.x, self.y, self.klass = t, [], [], [], None

        for n, s in enumerate(t):
            # Generate Nums and Syms from column names
            col = Num(n, s) if re.findall("^[A-Z]+", s) else Sym(n, s)
            self.all.append(col)

            if not re.findall("X$", s):
                if re.findall("!$", s):
                    self.klass = col

                if re.findall("[!+-]$", s):
                    # re.match("[!+-]$", s) and self.y or self.x, 
                    self.y.append(col)
                else:
                    self.x.append(col)

    def add(self, row: Row) -> None:
        """
        Updates the columns with details from row

        :param row: Row to add
        """
        for _, t in enumerate(zip(self.x, self.y)):
            for _, col in enumerate(t):
                col.add(row.cells[col.at])
