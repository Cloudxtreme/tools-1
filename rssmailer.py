#!/usr/bin/env python

# Module:   rssmailer
# Date:     9th January 2009
# Author:   James Mills, jmills at vision6 dot com dot au

"""RSS Mailer

A command line tool that downloads updates of a set of configured
RSS feeds and emails any new updates found to the email addresses
specified by the configuration.

This tool is ideally used via a cron job periodically.
"""

__version__ = "0.0.1"
__author__ = "James Mills, jmills at vision6 dot com dot au"

import os
import optparse
from hashlib import md5
import cPickle as pickle
from time import mktime, time
from StringIO import StringIO
from ConfigParser import ConfigParser

import feedparser

from pymills.utils import notags
from pymills.web import unescape

USAGE = "%prog [options]"
VERSION = "%prog v" + __version__

###
### Functions
###

def parse_options():
    """parse_options() -> opts, args

    Parse any command-line options given returning both
    the parsed options and arguments.
    """

    parser = optparse.OptionParser(usage=USAGE, version=VERSION)

    parser.add_option("-u", "--update",
            action="store_true", default=False, dest="update",
            help="Update feeds and email new items")
    parser.add_option("-a", "--add",
            action="store", default=None, dest="add",
            help="Add url as a new feed")
    parser.add_option("-r", "--remove",
            action="store", type="int", default=None, dest="remove",
            help="Remove spcified feed")
    parser.add_option("-l", "--list",
            action="store_true", default=False, dest="list",
            help="List all feeds")

    opts, args = parser.parse_args()

    return opts, args

def update(feeds, config):
    pass

###
### Classes
###

class Config(ConfigParser):

    def __init__(self, *args, **kwargs):
        ConfigParser.__init__(self, *args, **kwargs)

        self.filename = os.path.expanduser("~/.rssmailer/config.ini")

    def load(self):
        self.read(self.filename)

class Feeds(list):

    def __init__(self, *args, **kwargs):
        super(Feeds, self).__init__(*args, **kwargs)

        self.filename = os.path.expanduser("~/.rssmailer/feeds")

    def __str__(self):
        s = StringIO()
        s.write("Feeds: %d\n\n" % len(self))
        for i, feed in enumerate(self):
            s.write("%d. %s\n" % ((i + 1), feed))
        v = s.getvalue()
        s.close()
        return v

    def load(self):
        with open(self.filename, "r") as fd:
            for line in fd:
                self.append(line.strip())

    def save(self):
        with open(self.filename, "w") as fd:
            for feed in self:
                fd.write("%s\n" % feed)

class Feed(object):

    def __init__(self, url):
        self.url = url

        self.entries = []
        self.title = ""
        self.link = ""

    def getItems(self):
        d = feedparser.parse(self.url)

        if self.title == "" and self.link == "":
            self.title = d.feed.title
            self.link = d.feed.link

        new = []
        for v in d.entries:
            e = {
                    "time": mktime(v.updated_parsed),
                    "title": v.title,
                    "summary": unescape(
                        notags(v.summary).strip().split("\n")[0]),
                    "link": v.links[0].href
                    }

            if e not in self.entries:
                self.entries.append(e)
                new.append(e)

        if not new == []:
            s = []
            s.append("RSS: %s (%s)" % (
                self.title, self.link))
            for e in new[:3]:
                x = sum([
                    len(e["title"]),
                    len(e["summary"]),
                    len(e["link"])])
                if x > 450:
                    y = sum([
                        len(e["title"]),
                        len(e["link"])])
                    s.append(" * %s: %s ... <%s>" % (
                        e["title"],
                        e["summary"][:(450 - y)],
                        e["link"]))
                else:
                    s.append(" * %s: %s <%s>" % (
                        e["title"], e["summary"], e["link"]))
            return s
        else:
            return []


###
### Main
###

def main():
    opts, args = parse_options()

    feeds = Feeds()
    feeds.load()

    config = Config()
    config.load()

    if opts.add:
        feeds.append(opts.add)
        feeds.save()
    elif opts.remove:
        try:
            del feeds[(opts.remove - 1)]
            feeds.save()
        except Exception, error:
            print "ERROR: %s" % error
            raise SystemExit, 1
    elif opts.list:
        print feeds
    elif opts.update:
        update(feeds, config)
    else:
        print "No option specified, use --help for more usage information."
        raise SystemExit, 1

###
### Entry Point
###

if __name__ == "__main__":
    main()
