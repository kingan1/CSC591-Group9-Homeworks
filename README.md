
# CSC 591 HW1

![tests](https://github.com/kingan1/CSC591HW1/actions/workflows/tests.yml/badge.svg)
[![DOI](https://zenodo.org/badge/589679494.svg)](https://zenodo.org/badge/latestdoi/589679494)


Group members: Pradyumma Khawas, Jainam Shah, Ashley King

## About

HW1 for CSC591, onScript. Shows converting a .lua script to a .python script.

## Requirements

- Python 3.8 or higher

## How to run

- Clone the repository
    - run `git clone https://github.com/kingan1/CSC591HW1.git`
- Change to `src` directory
    - run `cd src`
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

- `python3 script.py -g the` or `python3 script.py -g all`
```
{'dump': False, 'go': 'the', 'help': False, 'seed': 937162211}
✅ pass: the
```
