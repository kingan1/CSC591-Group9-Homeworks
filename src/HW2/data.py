from num import Num
from sym import SYM
from options import Options
import random

options = Options()
help = """
script.py : an example script with help text and a test suite
(c)2023

USAGE:   script.py  [OPTIONS] [-g ACTION]

OPTIONS:
  -d  --dump  on crash, dump stack = false
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

def regenerate():
    num1,num2 = Num(),Num()
    random.seed(options['seed'])
    for i in range(1,10**3+1):
        num1.add( random.random() )
    random.seed(options['seed'])
    for i in range(1,10**3+1):
        num2.add( random.random() )
    m1,m2 = round(num1.mid(),10), round(num2.mid(),10)
    return m1==m2 and .5 == round(m1,1)

def check_syms():
    sym=SYM()
    for x in ["a","a","a","a","b","b","c"]:
        sym.add(x) 
    return "a"==sym.mid() and 1.379 == round(sym.div(), 3)

def check_nums():
    num=Num()
    for x in [1,1,1,1,2,2,3]:
        num.add(x) 
    return 11/7 == num.mid() and 0.787 == round(num.div(), 3) 


eg("the", "show settings", show_settings)

eg("rand","generate, reset, regenerate same", regenerate)

eg("sym","check syms", check_syms)

eg("num", "check nums", check_nums)

main(egs)
