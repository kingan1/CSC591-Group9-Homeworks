import random
from options import options
from num import Num
from stats import samples, gaussian
from utils import cliffsDelta

help = """

stats: shows different statistical methods
(c) Group 9
  
USAGE: python3 main.py [OPTIONS] [-g ACTIONS]
  
OPTIONS:
  -h  --help    show help                            = false
  -g  --go      start-up action                      = all
  -b  --bootstrap   number of samples to bootstrap   = 512
  -o  --conf   confidence interval                   = 0.05
  -c  --cliff   cliff cutoff point                   = 0.4
  -h  --cohen   cohen's D value                      = 0.35
  -w  --width   width                                = 40
  -f  --Fmt     format string                        = {:6.2f}
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
    
                if funs[what]() is False:
                    fails = fails + 1
                    print("❌ fail:", what, "-"*60)
                else:
                    print("✅ pass:", what, "-"*60)
    exit(fails)


# Examples
egs = {}


def eg(key, s, fun):
    global help
    egs[key] = fun
    help += "  -g  {}\t{}\n".format(key, s)

n=1
def check_ok():
    random.seed(n)

def check_sample(): 
    for i in range(1,10): 
        print("\t" + "".join(samples(["a","b","c","d","e"])))


def check_num():
  n=Num([1,2,3,4,5,6,7,8,9,10])
  print("\t",n.n, n.mu, n.sd)


def check_gauss():
    t=[]
    for i in range(10**4):
        t.append(gaussian(10,2))
    n=Num(t)
    print("\t",n.n,n.mu,n.sd)


def check_basic():
    print(
        "\t\ttrue",
        bootstrap({8, 7, 6, 2, 5, 8, 7, 3}, {8, 7, 6, 2, 5, 8, 7, 3}),
        cliffsDelta({8, 7, 6, 2, 5, 8, 7, 3}, {8, 7, 6, 2, 5, 8, 7, 3})
    )

    print(
        "\t\tfalse",
        bootstrap({8, 7, 6, 2, 5, 8, 7, 3}, {9, 9, 7, 8, 10, 9, 6}),
        cliffsDelta({8, 7, 6, 2, 5, 8, 7, 3}, {9, 9, 7, 8, 10, 9, 6})
    )

    print(
        "\t\tfalse",
        bootstrap({0.34, 0.49, 0.51, 0.6, .34, .49, .51, .6}, {0.6, 0.7, 0.8, 0.9, .6, .7, .8, .9}),
        cliffsDelta({0.34, 0.49, 0.51, 0.6, .34, .49, .51, .6}, {0.6, 0.7, 0.8, 0.9, .6, .7, .8, .9})
    )


eg("ok", "check ok", check_ok)
eg("sample", "check sample", check_sample)
eg("num", "check num", check_num)
eg("gauss", "check gauss", check_gauss)

if __name__ == "__main__":
    main(egs)
