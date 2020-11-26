import urllib.request, urllib.error
import os.path
import sys
import argparse
import json

def get_args():
    """Return arguments passed to the script"""
    parser = argparse.ArgumentParser()
    parser.add_argument('year',help='which year to get data from')
    parser.add_argument('day',help='which day to get data from')
    parser.add_argument('-p','--puzzle',help='dictates script to get the puzzle description', action='store_false', dest='input')
    parser.add_argument('-i','--input',help='dicates script to return just the puzzle input', action='store_false', dest='puzzle')
    parser.add_argument('-s','--session-cookie',help='set your session cookie')
    args = parser.parse_args()
    return args


def get_page(local_file: str, url: str, cookie = None):
    """Return the AOC page, sends a request if it isn't available locally"""
    page = None

    if os.path.isfile(local_file):
        with open(local_file,'r') as f:
            page = f.read()
    else:
        request = urllib.request.Request(url)
        if cookie:
            request.add_header('Cookie', 'session={}'.format(cookie))
        try:
            with urllib.request.urlopen(request) as response:
                page = response.read().decode('utf-8)')
        except urllib.error.URLError as e:
            print("{}: Could not GET '{}'.".format(str(e).split(':')[0] , request.get_full_url()), file=sys.stderr)
            exit(1)

        with open(local_file, 'w') as f:
            f.write(page)

    return page


def store_session_cookie(cookie: str, path='aoc-session-cookie.json'):
    """Writes cookie to file"""
    cookie = {'session-cookie': cookie}
    with open(path, 'w') as f:
        f.write(json.dumps(cookie))


def read_session_cookie(path='aoc-session-cookie.json'):
    """Reads cookie from file"""
    data = None
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        print("Could not find '{}'.".format(path), file=sys.stderr)
        exit(1)

    return data.get('session-cookie')


if __name__ == '__main__':
    args = get_args()
    results = []

    if args.session_cookie:
        store_session_cookie(args.session_cookie)
        cookie = args.session_cookie

    if args.puzzle:
        # get the puzzle
        local_file = 'aoc-{}-{}.html'.format(args.year, args.day)
        url = 'https://adventofcode.com/{}/day/{}'.format(args.year, args.day)
        get_page(local_file, url)
        results.append(local_file)

    if args.input:
        # get the input
        cookie = read_session_cookie()
        local_file = 'aoc-{}-{}-input.html'.format(args.year, args.day)
        url = 'https://adventofcode.com/{}/day/{}/input'.format(args.year, args.day)
        get_page(local_file, url, cookie)
        results.append(local_file)

    print('* Advent Of Code *')
    for result in results:
        print('=>',result)
