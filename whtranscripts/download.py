#!/usr/bin/env python
import sys, os
import lxml.html
import requests
import argparse
import itertools
from six.moves.urllib.parse import urlparse
import datetime as dt

flatten = lambda x: list(itertools.chain.from_iterable(x))

THIS_YEAR = dt.datetime.today().year
PRESIDENCY_BASE = "http://www.presidency.ucsb.edu/"    

ENDPOINTS = {
    "briefing": PRESIDENCY_BASE + "press_briefings.php",
    "conference": PRESIDENCY_BASE + "news_conferences.php"
}

START_YEARS = {
    "briefing": 1993,
    "conference": 1929
}

def norm_url(url):
    parsed = urlparse(url)
    normed_path = os.path.normpath(parsed.path)
    return "{0}://{1}{2}?{3}".format(
        parsed.scheme,
        parsed.netloc,
        normed_path,
        parsed.query
    )

def get_results_page_urls(year, doc_type):
    url = ENDPOINTS[doc_type]
    sys.stderr.write("Fetching {0}s from {1}\n".format(doc_type, year))
    press_html = requests.get(url, params={
        "year": year,
        "Submit": "DISPLAY"
    }).content
    press_dom = lxml.html.fromstring(press_html)
    press_dom.make_links_absolute(url)
    listed_links = press_dom.cssselect(".listdate a")
    page_urls = [ norm_url(a.attrib["href"]) for a in listed_links ]
    return page_urls

class Page(object):
    def __init__(self, url):
        self.url = url

    def get_html(self):
        sys.stderr.write("Grabbing {0} html\n".format(self.url))
        return requests.get(self.url).content

    def download(self, directory):
        html = self.get_html()
        f_name = self.url.split("=")[1]+".html"
        dest = os.path.join(directory, f_name)
        with open(dest, "w") as f:
            f.write(html)

def get_urls(doc_type, start_year=None, end_year=None):
    start_year = start_year or START_YEARS[doc_type]
    end_year = end_year or THIS_YEAR
    years = range(start_year, end_year + 1)
    urls = [ get_results_page_urls(y, doc_type) for y in years ]
    flat = flatten(urls)
    return flat

def parse_args():
    parser = argparse.ArgumentParser(description="""
        Download press briefings and news conferences from
        The American Presidency Project.""")
    parser.add_argument("--type", "-t",
        dest="doc_type",
        required=True,
        choices=[ "conference", "briefing" ],
        help="News conference or press briefing?")
    parser.add_argument("--dest",
        default=os.getcwd(),
        help="Destination directory for downloaded HTML files. Default is current working directory.")
    parser.add_argument("--start",
        type=int,
        help="Download only transcripts on or after year X.")
    parser.add_argument("--end",
        type=int,
        help="Download only transcripts on or before year X.")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    urls = get_urls(args.doc_type, args.start, args.end)
    pages = map(Page, urls)
    for page in pages:
        page.download(args.dest)
    
if __name__ == "__main__":
    main()
