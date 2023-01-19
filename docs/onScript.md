# HW1 - Scripts

Doc file for the [script.py](../src/HW1/script.py) file for Homework 1

## How to run

- To view the help string, run `python3 script.py --help`
- To run all tests, run `python3 script.py -g all`

## Command-line Options

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

## Examples

- `python3 script.py -g all`
```
{'dump': False, 'go': 'the', 'help': False, 'seed': 937162211}
✅ pass: the
```