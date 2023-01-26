from num import Num
from options import Options
from sym import Sym
from utils import rnd, rand, set_seed, csv

options = Options()
help = """
data.py : an example csv reader script
(c)2023

USAGE:   data.pu  [OPTIONS] [-g ACTION]

OPTIONS:
  -d  --dump  on crash, dump stack = false
  -f  --file  name of file         = ../../etc/data/auto93.csv
  -g  --go    start-up action      = data
  -h  --help  show help            = false
  -s  --seed  random number seed   = 937162211

ACTIONS:
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


eg("the", "show settings", show_settings)
eg("sym", "check syms", check_syms)
eg("num", "check nums", check_nums)
eg("csv", "read from csv", check_csv)
main(egs)
