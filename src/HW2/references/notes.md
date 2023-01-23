# Changed stuff

This doesn't need to be changed line by line but what was changed when I did a diff

- update the help string to match data.lua
- have global vars for:
```lua
local Seed,rand,rint,rnd --maths
local map,kap,sort,keys,push --lists
local fmt,oo,o,coerce,csv --stringsx
local settings, cli,main --settings
local NUM,SYM,ROW,COLS,DATA = obj"NUM",obj"SYM",obj"ROW",obj"COLS",obj"DATA"
```
- for SYM
  - include variable in the `init` method for at, txt
    - within init, `  i.at, i.txt = at or 0, txt or "" -- col position and name`
  - have a `rnd(self, x, n)` method that returns x
- for NUM
  - include variable in the `init` method for at, txt
    - within init, `  i.at, i.txt = at or 0, txt or "" -- col position and name`
    - keep the `i.n, i.mu, i.m2 = 0,0,0` and lo/hi line
    - add `i.w = i.txt:find"-$" and -1 or 1 end`
  - add method, add a `d` argument
    - don't make `d` local
  - add `function NUM.rnd(i,x,n) return x=="?" and x or rnd(x,n) end`
- new COLS class
- new ROW class
- new DATA class
- add a csv method
- update tests