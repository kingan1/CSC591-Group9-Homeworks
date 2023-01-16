import re
import sys

arg = sys.argv
the, help = {}, """
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


# Main

# attempts to convert v to an int, float, bool, or keep as string
def coerce(v):
    try:
        return int(v)
    except:
        try:
            return float(v)
        except:
            try:
                if v == True or v == False or v.lower() in ["true", "false"]:
                    return v.lower() == "true"
                return v
            except:
                return v


# Strings
def settings(s):  # parse help string to extract a table of options
  t = {}
  s = re.findall("\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s)
  for k, v in s:
    t[k] = coerce(v)
  return t

# print `t` then return it
def oo(t):
    print(t)
    return t

# update key,vals in `t` from command-line flags
def cli(options):
  for k, v in options.items():  # for each possible option / CLI
    v = str(v)  # get the default value
    for n, x in enumerate(arg):  # for each CLI passed in by the user
        if x == "-" + k[0] or x == "--" + k:  # if it matches one of the CLI
            v = ( arg[n+1] if n+1 < len(arg) else False) or v == "False" and "true" or v == "True" and "false"
            # set the value
        options[k] = coerce(v)
  return options

# `main` fills in the settings, updates them from the command line, runs
#  the start up actions (and before each run, it resets the random number seed and settongs);
#  and, finally, returns the number of test crashed to the operating system.
def main(options, help, funs, k=None, saved=None, fails=None):
    saved, fails = {}, 0
    for k, v in cli(settings(help)).items():
        options[k] = v
        saved[k] = v
    if options['help']:
        print(help)
    else:
        for what, fun in funs.items():
            if options['go'] == "all" or what == options['go']:
                for k, v in saved.items():
                    options[k] = v
                Seed = options['seed']
                if funs[what]() == False:
                    fails = fails+1
                    print("❌ fail:", what)
                else:
                    print("✅ pass:", what)
    exit(fails)


# Examples
egs = {}
# --> nil; register an example.
def eg(key, s, fun):
    global help
    egs[key]=fun
    help += "  -g  {}\t{}\n".format(key,s)

  
# eg("crash","show crashing behavior", function()
#   return the.some.missing.nested.field )

def f():
    return oo(the)


eg("the","show settings", f)

# eg("rand","generate, reset, regenerate same", function()
#   local num1,num2 = NUM(),NUM()
#   Seed=the.seed; for i=1,10^3 do num1:add( rand(0,1) ) 
#   Seed=the.seed; for i=1,10^3 do num2:add( rand(0,1) ) 
#   local m1,m2 = rnd(num1:mid(),10), rnd(num2:mid(),10)
#   return m1==m2 and .5 == rnd(m1,1)  )

# eg("sym","check syms", function()
#   local sym=SYM()
#   for _,x in pairs{"a","a","a","a","b","b","c"} do sym:add(x) 
#   return "a"==sym:mid() and 1.379 == rnd(sym:div()))

# eg("num", "check nums", function()
#   local num=NUM()
#   for _,x in pairs{1,1,1,1,2,2,3} do num:add(x) 
#   return 11/7 == num:mid() and 0.787 == rnd(num:div())  )

main(the,help, egs)
