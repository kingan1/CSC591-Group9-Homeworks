from num import Num
from sym import Sym
import re
from utils import csv

# -- ### COLS
# -- Factory for managing a set of NUMs or SYMs
class COLS:
    def __init__(self,t): # --> COLS; generate NUMs and SYMs from column names
        self.names, self.all, self.x, self.y, self.klass = t, [], [], [], None
        for n,s in enumerate(t):
            col = Num(n,s)  if re.findall("^[A-Z]+", s) else Sym(n,s)
            self.all.append(col)
            if not re.findall("X$", s):
                if re.findall("!$", s): 
                    self.klass = col 
                if re.findall("[!+-]$", s) :
                    # re.match("[!+-]$", s) and self.y or self.x, 
                    self.y.append(col)
                else:
                    self.x.append(col)

    def add(self,row): # nil; update the (not skipped) columns with details from `row`
        for _,t in enumerate(zip(self.x,self.y)): 
            for _,col in enumerate(t):
                col.add(row.cells[col.at])

