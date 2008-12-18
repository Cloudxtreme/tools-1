#!/usr/bin/env python

# Module:	csvreader
# Date:		6th June 2008
# Author:	James Mills, prologic at shortcircuit dot net dot au

"""csvreader

Tool to read and parse CSV files into useable pieces
of data that can be used in other systems or in other
ways. Example: Converting CSV files to SQL.
"""

__desc__ = "CSV Reader"
__version__ = "0.2"
__author__ = "James Mills"
__email__ = "%s, prologic at shortcircuit dot net dot au" % __author__
__url__ = "http://shortcircuit.net.au/~prologic/"
__copyright__ = "CopyRight (C) 2005-2008 by %s" % __author__
__license__ = "GPL"

import csv
import optparse
from cStringIO import StringIO

USAGE = "%prog [options] <file>"
VERSION = "%prog v" + __version__

def parse_options():
	"""parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.
	"""

	parser = optparse.OptionParser(usage=USAGE, version=VERSION)

	opts, args = parser.parse_args()

	if len(args) < 1:
		parser.print_help()
		raise SystemExit, 1

	return opts, args

def readCSV(file):

	if type(file) == str:
		fd = open(file, "rU")
	else:
		fd = file

	sniffer = csv.Sniffer()
	dialect = sniffer.sniff(fd.readline())
	fd.seek(0)

	reader = csv.reader(fd, dialect)
	for line in reader:
		yield line

def main():
	opts, args = parse_options()

	file = args[0]

	if file == "-":
		fd = sys.stdin
	else:
		fd = open(file, "rU")

	for line in readCSV(fd):
		print line

if __name__ == "__main__":
	main()
