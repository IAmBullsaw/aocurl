# aocurl
Downloads advent of code puzzles and inputs.
To not abuse the server, if you've already downloaded the files previously this will just look inside the folder `~/.aocurl/`


## Usage

### First use
First use you need to set your (session-cookie)[#retrieve-your-session-cookie]

```bash
$ python3 aocurl.py 2020 1 -s session-cookie
```

Or already have it saved to a file named aoc-session-cookie.json within the root folder `~/.aocurl/`

```bash
$ cat aoc-session-cookie.json
{"session-cookie": "1234...abcde"}
```

### Standard use
When set the normal usage would look like this
```bash
$ python3 aocurl.py 2020 1
/home/$USER/.aocurl/aoc-2020-1.html
/home/$USER/.aocurl/aoc-2020-1-1.txt
/home/$USER/.aocurl/aoc-2020-1-input.txt
```

The produced files are

`/home/$USER/.aocurl/aoc-2020-1.html` the full html
`/home/$USER/.aocurl/aoc-2020-1-1.txt` is the description for the requested day level 1, level two would be `../aoc-2020-1-2.txt`
`/home/$USER/.aocurl/aoc-2020-1-input.txt` is the input for the requested day

### Submitting an answer
When you have gotten an answer, let's say you got `4711`, you can submit your answer with 

```bash
$ python3 aocurl.py 2020 1 -a 1 4711
Correct!
```

### Getting the next levels instructions 
If you have submitted a correct answer, you might want to retrieve the next part of the puzzle, i.e level 2. To do this, you need to refetch the whole day from the server, so you have to use `--force`.

```bash
$ python3 aocurl.py 2020 1 -pf
/home/$USER/.aocurl/aoc-2020-1.html
/home/$USER/.aocurl/aoc-2020-1-1.txt
/home/$USER/.aocurl/aoc-2020-1-2.txt
```

Please do not forget `-p` to not refetch the input

### Using aocurl as the input for your solution
If you want, you can fetch and send a days input to stdout and pipe it to your solution

```bash
$ python3 aocurl.py 2020 1 -io | ./solution
```


### Full usage
Full usage can be found via argparses -h
```bash
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

## Retrieve your session cookie
It's easy but not entirely trivial to find your session cookie. Good news is that this cookie is valid for a whole month, so you probably only need to do this step once for the whole competition!

1. Go to www.adventofcode.com and log in
2. In the browser, do Inspect element (There's usually an option for this in the right click menu)
3. Find the request to www.adventofcode.com and look for the cookie
