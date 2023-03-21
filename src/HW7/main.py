from options import options

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

if __name__ == "__main__":
    main(egs)
