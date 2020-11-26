# aocurl
Downloads advent of code puzzles and inputs.
To not abuse the server, if you've already downloaded the files previously this will just look inside the folder `~/.aocurl/`


## Usage

First use you need to set your session-cookie

```
$ python3 aocurl.py 2020 1 -s session-cookie
```

Or already have it saved to a file named aoc-session-cookie.json within the root folder `~/.aocurl/`

```
$ cat aoc-session-cookie.json 
{"session-cookie": "53616c7465645f5f4b461f6bbb4c4414bd69e9e3bde29fb0a1680a3bcefd03a00f1486ee76573192d01b7eca0fe7c21e"}
```

Full usage can be found via argparses -h
```
usage: aocurl.py [-h] [-p] [-i] [-s SESSION_COOKIE] year day

positional arguments:
  year                  which year to get data from
  day                   which day to get data from

optional arguments:
  -h, --help            show this help message and exit
  -p, --puzzle          dictates script to get the puzzle description
  -i, --input           dicates script to return just the puzzle input
  -s SESSION_COOKIE, --session-cookie SESSION_COOKIE
                        set your session cookie
```
