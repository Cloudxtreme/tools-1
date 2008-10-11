#!/usr/bin/env python

# Module:	csvcut
# Date:		3rd October 2008
# Author:	James Mills, prologic at shortcircuit dot net dot au

"""csvcut

Tool to read and cut up CSV files by fields.
"""

__desc__ = "CSV Cut"
__version__ = "0.2.3"
__author__ = "James Mills"
__email__ = "%s, prologic at shortcircuit dot net dot au" % __author__
__url__ = "http://shortcircuit.net.au/~prologic/"
__copyright__ = "CopyRight (C) 2005-2008 by %s" % __author__
__license__ = "GPL"

import sys
import csv
import optparse
from cStringIO import StringIO

USAGE = "%prog [options] [file]"
VERSION = "%prog v" + __version__

def parse_options():
	"""parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.
	"""

	parser = optparse.OptionParser(usage=USAGE, version=VERSION)

	parser.add_option("-f", "--fields",
			action="store", type="string", default=None, dest="fields",
			help="List of fields to cut")

	opts, args = parser.parse_args()

	if not opts.fields:
		print "ERROR: No fields specified, use -f/--fields"
		parser.print_help()
		raise SystemExit, 1

	return opts, args

def mkBuffer(fd):
	buffer = StringIO()
	buffer.write(fd.read())
	buffer.seek(0)
	fd.close()
	return buffer

def readCSV(file):

	if type(file) == str:
		fd = open(file, "rU")
	else:
		fd = file

	fd = mkBuffer(fd)

	sniffer = csv.Sniffer()
	dialect = sniffer.sniff(fd.readline())
	fd.seek(0)

	reader = csv.reader(fd, dialect)
	for line in reader:
		yield line

def main():
	opts, args = parse_options()

	if args:
		fd = open(args[0], "rU")
	else:
		fd = sys.stdin

	if opts.fields:
		fields = [int(x) for x in fields.split(",")]
	else:
		fields = None

	for line in readCSV(fd):
		if fields:
			s = []
			for x in fields:
				s.append(line[x])
			print ",".join(s)
		else:
			print line

if __name__ == "__main__":
	main()
