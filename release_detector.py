#!/usr/bin/env python

import argparse
import urllib
import sys
import os.path
from HTMLParser import HTMLParser
import re
import datetime

'''
ArgumentParser Settigs.
'''
parser = argparse.ArgumentParser(description='This script is update detection for the AppStore.')
parser.add_argument('-u', '--url', type=str, required=True, nargs=1,  help="Store url.")
args = parser.parse_args()

'''
Before file path.
'''
before_file_path = './tmp/before_date.txt'

'''
Parser
'''
class AndroidVersionParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.isDatePublished = False
        self.date = ''

    '''
    ' Find software date tag.
    '''
    def handle_starttag(self, tag, attrs):
        self.isDatePublished = False 
        attrs = dict(attrs)
        if tag != 'span':
            return
        if 'itemprop' not in attrs:
            return
        if attrs['itemprop'] != 'datePublished':
            return
        self.isDatePublished = True

    '''
    ' Extraction date data.
    '''
    def handle_data(self, data):
        data = data.strip('\ \n')
        if not self.isDatePublished:
            return
        if not data:
            return
        self.date = data
def WriteDate(date):
    f = open(before_file_path, 'w')
    f.write(date)
    f.close()

def ReadDate():
    f = open(before_file_path)
    date = f.read()
    f.close()
    split_pattern = r"\D"
    arr = re.split(split_pattern, date)
    strdate = '-'.join(filter(None, arr))
    return strdate

'''
Main.
'''
if __name__ == "__main__":
    # Get Parser
    parser = AndroidVersionParser()
    if not parser:
        print 'none parser.'
        sys.exit(1)
    # Parse
    url = args.url[0]
    parser.feed(unicode(urllib.urlopen(url).read(), "utf-8"))

    if not parser.date:
        print 'cannot parse.'
        sys.exit(2)
    
    # Check updated date.
    split_pattern = r"\D"
    arr = re.split(split_pattern, parser.date)
    strdate = '-'.join(filter(None, arr))
    updated = datetime.datetime.strptime(strdate, '%Y-%m-%d')

    # First run.
    if not os.path.isfile(before_file_path):
        print 'Detected!'
        print 'date:', updated.isoformat()
        WriteDate(strdate)
        sys.exit(0)

    # Read date from before date file.
    date = ReadDate()
    before_date = datetime.datetime.strptime(date, '%Y-%m-%d')

    # Detect the difference of updated.
    if before_date != updated:
        print 'Updated!'
        print 'date:', updated.isoformat()
        WriteDate(strdate)
    sys.exit(0)
