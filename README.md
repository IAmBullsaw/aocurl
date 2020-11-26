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
{"session-cookie": "1234...abcde"}
```

Full usage can be found via argparses -h
```
usage: aocurl.py [-h] [--version] [-p] [-i] [-s SESSION_COOKIE] [-o] [-f] [-a ANSWER ANSWER] [-l] year day

positional arguments:
  year                  which year to get data from
  day                   which day to get data from

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -p, --puzzle          dictates script to get the puzzle description
  -i, --input           dicates script to return just the puzzle input
  -s SESSION_COOKIE, --session-cookie SESSION_COOKIE
                        set your session cookie
  -o, --output          send results to stdout
  -f, --force           forces to GET from advent of code
  -a ANSWER ANSWER, --answer ANSWER ANSWER
                        send answer to adventofcode (level answer)
  -l, --look_at_stats   see your local stats

```
