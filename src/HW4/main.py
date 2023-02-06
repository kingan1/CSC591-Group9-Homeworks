from data import Data
from num import Num
from options import options
from sym import Sym
from utils import rnd, csv, show, transpose

help = """
main.py : a rep grid processor
(c)2023

USAGE:   main.py  [OPTIONS] [-g ACTION]

OPTIONS:
  -d  --dump    on crash, dump stack   = false
  -f  --file    name of file           = ../../etc/data/repgrid1.csv
  -g  --go      start-up action        = data
  -h  --help    show help              = false
  -p  --p       distance coefficient   = 2
  -s  --seed    random number seed     = 937162211
"""


def main(funs, saved=None, fails=None):
    """
    `main` fills in the settings, updates them from the command line, runs
    the start up actions (and before each run, it resets the random number seed and settongs);
    and, finally, returns the number of test crashed to the operating system.

    :param funs: list of actions to run
    :param saved: dictionary to store options
    :param fails: number of failed functions
    """

    saved, fails = {}, 0
    options.parse_cli_settings(help)

    for k, v in options.items():
        saved[k] = v

    if options['help']:
        print(help)
    else:
        for what, fun in funs.items():
            if options['go'] == "all" or what == options['go']:
                for k, v in saved.items():
                    options[k] = v

                if funs[what]() is False:
                    fails = fails + 1
                    print("❌ fail:", what)
                else:
                    print("✅ pass:", what)
    exit(fails)


# Examples
egs = {}


def eg(key, s, fun):
    global help
    egs[key] = fun
    help += "  -g  {}\t{}\n".format(key, s)


def show_settings():
    return str(options)


def check_syms():
    sym = Sym()

    for x in ["a", "a", "a", "a", "b", "b", "c"]:
        sym.add(x)

    return "a" == sym.mid() and 1.379 == rnd(sym.div(), 3)


def check_nums():
    num = Num()

    for x in [1, 1, 1, 1, 2, 2, 3]:
        num.add(x)

    return 11 / 7 == num.mid() and 0.787 == rnd(num.div(), 3)


def check_csv():
    n = 0

    def f(t):
        nonlocal n
        n += len(t)

    csv(options['file'], f)
    return n == 8 * 399


def check_data():
    data = Data(options["file"])

    return len(data.rows) == 398 and data.cols.y[0].w == -1 and data.cols.x[0].at == 0 and len(data.cols.x) == 4


def check_clone():
    data1 = Data(options["file"])
    data2 = data1.clone(data1.rows)

    return (
        len(data1.rows) == len(data2.rows)
        and data1.cols.y[1].w == data2.cols.y[1].w
        and data1.cols.x[1].at == data2.cols.x[1].at
        and len(data1.cols.x) == len(data2.cols.x)
    )


def check_stats():
    data = Data(options["file"])

    for k, cols in {"y": data.cols.y, "x": data.cols.x}.items():
        print(k, "\tmid\t", data.stats(cols, 2, what="mid"))
        print("", "\tdiv\t", data.stats(cols, 2, what="div"))


def check_half():
    data=Data(options['file'])
    left,right,A,B,mid,c = data.half() 
    print(len(left),len(right),len(data.rows))
    print(A.cells,c)
    print(mid.cells)
    print(B.cells)

def check_around():
    data=Data(options['file'])
    print(0,0,data.rows[0].cells)
    for n,t in enumerate(data.around(data.rows[0])):
        if (n+1) %50 ==0:
            print(n, rnd(t['dist'],2) ,t['row'].cells)


def check_cluster():
    data = Data(options['file'])

    show(data.cluster(), "mid", data.cols.y, 1)


def check_optimize():
    data = Data(options['file'])

    show(data.sway(), "mid", data.cols.y, 1)

def check_reprows():
    t = None
    exec(open(options['file']).read())
    rows = repRows(t, transpose(t.cols))
    print(rows.cols.all) 
    print(rows.rows) 


eg("around", "sorting nearest neighbors", check_around)
eg("clone", "duplicate structure", check_clone)
eg("cluster", "N-level bi-clustering", check_cluster)
eg("data", "read DATA csv", check_data)
eg("half", "1-level bi-clustering", check_half)
eg("num", "check nums", check_nums)
eg("optimize", "semi-supervised optimization", check_optimize)
eg("sym", "check syms", check_syms)
eg("the", "show settings", show_settings)
eg("reprows","checking reprows", check_reprows)

# eg("csv", "read from csv", check_csv)
# eg("stats", "stats from DATA", check_stats)
main(egs)
