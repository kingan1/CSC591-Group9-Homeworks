
# CSC 591 HW1

![tests](https://github.com/kingan1/CSC591HW1/actions/workflows/tests.yml/badge.svg)

Group members: Pradyumma Khawas, Jainam Shah, Ashley King

## How to run

From the src directory
- `python3 script.py --help`
```
script.py : an example script with help text and a test suite
(c)2023

USAGE:   script.py  [OPTIONS] [-g ACTION]

OPTIONS:
  -d  --dump  on crash, dump stack = false
  -g  --go    start-up action      = data
  -h  --help  show help            = false
  -s  --seed  random number seed   = 937162211

ACTIONS:
  -g  the       show settings
```
- `python3 script.py -g the` or `python3 script.py -g all`
```
{'dump': False, 'go': 'the', 'help': False, 'seed': 937162211}
✅ pass: the
```

## TODO

- Github "bling"
    - Run tests via github workflows & badge for it
    - Zenodo badges
- Version control
    - .gitignore
    - .github/workflows for tests
    - README.md
    - /etc for local config
    - /etc/out cache for experimental output logs
    - /src for code
- Tests (what is shown in script.lua)
    - sym
    - num
    - DONE: the
    - rand

### Lua file

`lua script.lua --help`
- Options
    - dump
    - go
    - help
    - seed
- Actions
    - the
    - rand
    - sm
    - num

## Overview
**_From Menzies on Discord_** 

"translate the Lua code to a language of our choice". 

to do so, for /src/X.lua, remember to read:
-  /docs/X.md 
-  /docs/onX.md. 

and try to generate the output in /etc/out/X.out .  when generating that output, near enough is good enough. 

apart from the code functionality, we also want to see  k code that:
- runs tests via the github workflows
- does long term storage in zenodo
- has code in multiple files (e.g. NUM.py, SYM.py, __init__.py, tests.py, utilis.py, config.py, etc) . how you split things up is up to you BUT if everything stays in ONE file then you get into all sorts of bother as everyone writes to that file

we also want to look at the GH logs and see lots of activity from everyone on the group. 

also, we want all the files and bling listed in https://github.com/timm/tested/blob/main/docs/onScript.md#version-contol

for advanced GH users, I offer this comment: consider NOT doing branches (ie. consider commit to main). why? this code  might be too tiny and your time frame might be  too short for branch-based development . but in the end, just do what works for your team. 
