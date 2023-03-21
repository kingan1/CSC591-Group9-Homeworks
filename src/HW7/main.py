import random
from options import options
from num import Num
from stats import samples, gaussian, RX, ScottKnott, tiles, bootstrap, cliffsDelta
from utils import mid

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
        bootstrap([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3]),
        cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3])
    )

    print(
        "\t\tfalse",
        bootstrap([8, 7, 6, 2, 5, 8, 7, 3], [9, 9, 7, 8, 10, 9, 6]),
        cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [9, 9, 7, 8, 10, 9, 6])
    )

    print(
        "\t\tfalse",
        bootstrap([0.34, 0.49, 0.51, 0.6, .34, .49, .51, .6], [0.6, 0.7, 0.8, 0.9, .6, .7, .8, .9]),
        cliffsDelta([0.34, 0.49, 0.51, 0.6, .34, .49, .51, .6], [0.6, 0.7, 0.8, 0.9, .6, .7, .8, .9])
    )


def check_pre():
    print("\neg3")
    d = 1

    for i in range(1,11):
        t1, t2 = [], []

        for j in range(1,32):
            t1.append(gaussian(10,1))
            t2.append(gaussian(d * 10,1))

        print("\t", f"{d:.2f}", d < 1.1 and "true" or "false", bootstrap(t1, t2), bootstrap(t1, t1))

        d += 0.05


def check_five():
    tiles_ = tiles(ScottKnott([
        RX({0.34, 0.49, 0.51, 0.6, .34, .49, .51, .6}, "rx1"),
        RX({0.6, 0.7, 0.8, 0.9, .6, .7, .8, .9}, "rx2"),
        RX({0.15, 0.25, 0.4, 0.35, 0.15, 0.25, 0.4, 0.35}, "rx3"),
        RX({0.6, 0.7, 0.8, 0.9, 0.6, 0.7, 0.8, 0.9}, "rx4"),
        RX({0.1, 0.2, 0.3, 0.4, 0.1, 0.2, 0.3, 0.4}, "rx5")
    ]).run())

    for rx in tiles_:
        print(rx["name"], rx["rank"], rx["show"])

def check_six():
    tiles_ = tiles(ScottKnott([
        RX({101,100,99,101,99.5,101,100,99,101,99.5}, "rx1"),
        RX({101,100,99,101,100,101,100,99,101,100}, "rx2"),
        RX({101,100,99.5,101,99,101,100,99.5,101,99}, "rx3"),
        RX({101,100,99,101,100,101,100,99,101,100}, "rx4")
    ]).run())

    for rx in tiles_:
        print(rx["name"], rx["rank"], rx["show"])

def check_tiles():
    rxs,a,b,c,d,e,f,g,h,j,k=[],[],[],[],[],[],[],[],[],[],[]
    upper_limit=1001
    for i in range(1,upper_limit):
        a.append(gaussian(10,1))
    for i in range(1,upper_limit):
        b.append(gaussian(10.1,1))
    for i in range(1,upper_limit):
        c.append(gaussian(20,1))
    for i in range(1,upper_limit):
        d.append(gaussian(30,1))
    for i in range(1,upper_limit):
        e.append(gaussian(30.1,1))
    for i in range(1,upper_limit):
        f.append(gaussian(10,1))
    for i in range(1,upper_limit):
        g.append(gaussian(10,1))
    for i in range(1,upper_limit):
        h.append(gaussian(40,1))
    for i in range(1,upper_limit):
        j.append(gaussian(40,3))
    for i in range(1,upper_limit):
        k.append(gaussian(10,1))

    for k, v in enumerate([a, b, c, d, e, f, g, h, j, k]):
        rxs.append(RX(v, "rx" + str(k + 1)))
    rxs.sort(key=lambda x: mid(x))
    for rx in tiles(rxs):
        print("", rx["name"], rx["show"])

def check_sk():
    rxs,a,b,c,d,e,f,g,h,j,k=[],[],[],[],[],[],[],[],[],[],[]
    upper_limit=1001
    for i in range(1,upper_limit):
        a.append(gaussian(10,1))
    for i in range(1,upper_limit):
        b.append(gaussian(10.1,1))
    for i in range(1,upper_limit):
        c.append(gaussian(20,1))
    for i in range(1,upper_limit):
        d.append(gaussian(30,1))
    for i in range(1,upper_limit):
        e.append(gaussian(30.1,1))
    for i in range(1,upper_limit):
        f.append(gaussian(10,1))
    for i in range(1,upper_limit):
        g.append(gaussian(10,1))
    for i in range(1,upper_limit):
        h.append(gaussian(40,1))
    for i in range(1,upper_limit):
        j.append(gaussian(40,3))
    for i in range(1,upper_limit):
        k.append(gaussian(10,1))

    for k, v in enumerate([a, b, c, d, e, f, g, h, j, k]):
        rxs.append(RX(v, "rx" + str(k + 1)))
    
    for rx in tiles(ScottKnott(rxs).run()):
        print("", rx['rank'], rx["name"], rx["show"])


eg("pre", "check pre", check_pre)
eg("ok", "check ok", check_ok)
eg("sample", "check sample", check_sample)
eg("num", "check num", check_num)
eg("gauss", "check gauss", check_gauss)
eg("basic", "check basic", check_basic)
eg("tiles","check tiles", check_tiles)
eg("sk","check sk", check_sk)
eg("five", "check five", check_five)
eg("six", "check six", check_six)

if __name__ == "__main__":
    main(egs)
