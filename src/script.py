from options import Options

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

"""
 `main` fills in the settings, updates them from the command line, runs
  the start up actions (and before each run, it resets the random number seed and settongs);
  and, finally, returns the number of test crashed to the operating system.

  :param funs: list of actions to run
  :param saved: dictionary to store options
  :param fails: number of failed functions
"""
def main(funs, saved=None, fails=None):
    saved, fails = {}, 0
    options.parseCliSettings(help)
    for k, v in options.items():
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
    return str(options)


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

main(egs)
