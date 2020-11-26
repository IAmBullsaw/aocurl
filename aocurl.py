import urllib.request
import urllib.error
from pathlib import Path
import os.path
import sys
import argparse
import json
from html.parser import HTMLParser


class AOCHTMLParser(HTMLParser):
    read = False
    articles = [[], []]
    article_no = -1

    def handle_starttag(self, tag, attrs):
        if tag == 'article':
            self.read = True
            self.article_no += 1
        # print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        if tag == 'article':
            self.read = False
            self.articles[self.article_no].insert(1, '\n')
            article = ''.join(self.articles[self.article_no])
            self.articles[self.article_no] = article

        # print("Encountered an end tag :", tag)

    def handle_data(self, data):
        if self.read:
            self.articles[self.article_no].append(data)


def get_args():
    """Return arguments passed to the script"""
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int, help='which year to get data from')
    parser.add_argument('day', type=int, help='which day to get data from')
    parser.add_argument('-p', '--puzzle', action='store_false', dest='input',
                        help='dictates script to get the puzzle description')
    parser.add_argument('-i', '--input', action='store_false', dest='puzzle',
                        help='dicates script to return just the puzzle input')
    parser.add_argument('-s', '--session-cookie',
                        help='set your session cookie')
    parser.add_argument('-o', '--output', action='store_true',
                        help='send results to stdout')
    parser.add_argument('-f', '--force', action='store_true',
                        help='forces to GET from advent of code')
    parser.add_argument('-a', '--answer', type=str, nargs=2,
                        help='send answer to adventofcode')
    # parser.add_argument('-l', '--leaderboard', help='see your leaderboard')

    args = parser.parse_args()
    return args


def get_page(local_file: str, url: str, cookie=None, force=False):
    """Return the AOC page, sends a request if it isn't available locally"""
    page = None

    if not force and os.path.isfile(local_file):
        with open(local_file, 'r') as f:
            page = f.read()
    else:
        request = urllib.request.Request(url)
        if cookie:
            request.add_header('Cookie', 'session={}'.format(cookie))
        try:
            with urllib.request.urlopen(request) as response:
                page = response.read().decode('utf-8)')
        except urllib.error.URLError as e:
            print("{}: Could not GET '{}'.".format(
                                str(e).split(':')[0],
                                request.get_full_url()),
                  file=sys.stderr)
            exit(1)

        with open(local_file, 'w') as f:
            f.write(page)

    return page


def store_session_cookie(cookie: str, path='aoc-session-cookie.json'):
    """Writes cookie to file"""
    cookie = {'session-cookie': cookie}
    local_file = get_local_file_path(path)
    with open(local_file, 'w') as f:
        f.write(json.dumps(cookie))


def read_session_cookie(path='aoc-session-cookie.json'):
    """Reads cookie from file"""
    data = None
    local_file = get_local_file_path(path)
    try:
        with open(local_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        print("Could not find '{}'.".format(local_file), file=sys.stderr)
        exit(2)

    return data.get('session-cookie')


def setup():
    """Creates ~/.aocurl if it does not exist"""
    home = str(Path.home())
    aocurl_home = home + '/.aocurl'
    if not os.path.isdir(aocurl_home):
        try:
            os.mkdir(aocurl_home)
        except OSError:
            print("Creation of the directory '{}' failed".format(aocurl_home),
                  file=sys.stderr)
            exit(3)


def get_local_file_path(path):
    """Return the absolute path to the passed in path"""
    home = str(Path.home())
    full_path = home + '/.aocurl/' + path
    return full_path


def parse_articles(html):
    """Returns the articles found in the html"""
    parser = AOCHTMLParser()
    parser.feed(html)
    return parser.articles


def parse_success(html):
    """Returns True if the html indicates a success. Exits if spamming."""
    parser = AOCHTMLParser()
    parser.feed(html)

    if 'You gave an answer too recently' in parser.articles[0]:
        print('Too many attempts!', file=sys.stderr)
        exit(1)

    if "You don't seem to be solving the right level" in parser.articles[0]:
        print('Already solved!', file=sys.stderr)
        exit(1)

    failure = "That's not the right answer" in parser.articles[0]
    return not failure


def post_answer(year, day, level, answer, cookie):
    """POST answer"""
    url = "https://adventofcode.com/{}/day/{}/answer".format(year, day)
    request = urllib.request.Request(url)
    request.add_header('Cookie', 'session={}'.format(cookie))
    data = urllib.parse.urlencode({'level': level, 'answer': answer})
    data = data.encode('ascii')
    try:
        with urllib.request.urlopen(request, data) as response:
            page = response.read().decode('utf-8)')
    except urllib.error.URLError as e:
        print("{}: Could not POST '{}'.".format(
                            str(e).split(':')[0],
                            request.get_full_url()),
              file=sys.stderr)
        exit(1)

    return page


if __name__ == '__main__':
    """Main script flow"""
    args = get_args()
    results = []

    setup()

    if args.session_cookie:
        store_session_cookie(args.session_cookie)
        cookie = args.session_cookie

    cookie = read_session_cookie()

    if args.answer:
        resp = post_answer(args.year, args.day,
                           args.answer[0], args.answer[1], cookie)
        if parse_success(resp):
            print('Correct!')
        else:
            print('Wrong!', file=sys.stderr)
        exit()

    if args.puzzle:
        local_file = get_local_file_path('aoc-{}-{}.html'.format(args.year,
                                                                 args.day))
        url = 'https://adventofcode.com/{}/day/{}'.format(args.year, args.day)
        page = get_page(local_file, url, cookie, args.force)
        results.append(local_file)
        if args.output:
            print(page)

    if args.input:
        local_file = get_local_file_path(
            'aoc-{}-{}-input.txt'.format(args.year, args.day))

        url = 'https://adventofcode.com/{}/day/{}/input'.format(args.year,
                                                                args.day)
        page = get_page(local_file, url, cookie, args.force)
        results.append(local_file)
        if args.output:
            print(page)

    if not args.output:
        # Print the absolute path to the sought after file(s)
        print('* Advent Of Code *')
        for result in results:
            print('=>', result)
