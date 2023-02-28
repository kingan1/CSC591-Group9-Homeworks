from typing import List, Dict, Tuple

from data import Data
from discretization import value, bins, Range
from utils import rnd


class Explain:
    def __init__(self, best: Data, rest: Data):
        self.best = best
        self.rest = rest

        self.tmp: List[Tuple[Range, int, float]] = []
        self.max_sizes: Dict[str, int] = {}

    def score(self, ranges: List[Range]):
        rule = self.rule(ranges, self.max_sizes)

        if rule:
            print(show_rule(rule))

            bestr = selects(rule, self.best.rows)
            restr = selects(rule, self.rest.rows)

            if len(bestr) + len(restr) > 0:
                return value({"best": len(bestr), "rest": len(restr)}, len(self.best.rows), len(self.rest.rows), "best")

    def xpln(self, data: Data, best: Data, rest: Data):
        for ranges in bins(data.cols.x, rowss={"best": best.rows, "rest": rest.rows}):
            self.max_sizes[ranges[1].txt] = len(ranges)

            for _range in ranges:
                print(_range.txt, _range.lo, _range.hi)

                self.tmp.append((_range, len(ranges), value(_range.y.has, len(best.rows), len(rest.rows), "best")))

            return self.first_n(sorted(self.tmp, key=lambda row: row[2], reverse=True))

    def first_n(self, sorted_ranges: List[Tuple[Range, int, float]]):
        for _range, _max, _val in sorted_ranges:
            print(_range.txt, _range.lo, _range.hi, rnd(_val), _range.y.has)

            first = sorted_ranges[0][2]
            sorted_ranges = [_range for _range in sorted_ranges if _val > 0.05 and _val > first / 10]

            most: int = -1
            out: int = -1

            for n in range(len(sorted_ranges)):
                tmp, rule = self.score([_range for _range, _max, _val in sorted_ranges[:n]])

                if tmp is not None and tmp > most:
                    out, most = rule, tmp

            return out, most
    
    def rule(self, ranges,maxSize):
        t={}
        for _,range in enumerate(ranges):
            t[range.txt] = t.get(range.txt, [])
            t[range.txt].append({"lo":range.lo,"hi":range.hi,"at":range.at})
        return self.prune(t, maxSize)

    def prune(self, rule, maxSize):
        n=0
        for txt,ranges in rule.items():
            n = n+1
            if len(ranges) == maxSize[txt]:
                n=n-1
                rule[txt] = None
            if n > 0: 
                return rule
        return None
