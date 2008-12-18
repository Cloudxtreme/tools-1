#!/usr/bin/env python

# Module:	csv2sql
# Date:		14th September 2008
# Author:	James Mills, prologic at shortcircuit dot net dot au

"""csv2sql

Tool to convert CSV data files into SQL statements that
can be used to create SQL tables. Each line of text in
the file is read, parsed and converted to SQL and output
to stdout (which can be piped).
"""

__desc__ = "CSV to SQL Tool"
__version__ = "0.3"
__author__ = "James Mills"
__email__ = "%s, prologic at shortcircuit dot net dot au" % __author__
__url__ = "http://shortcircuit.net.au/~prologic/"
__copyright__ = "CopyRight (C) 2008 by %s" % __author__
__license__ = "GPL"

import os
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

	parser.add_option("-t", "--table",
			action="store", default=None, dest="table",
			help="Specify table name")

	parser.add_option("-f", "--fields",
			action="store", default=None, dest="fields",
			help="Specify a list of fields")

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
		if opts.table is None:
			print "ERROR: No table specified and stdin used."
			raise SystemExit(1)
	else:
		fd = open(file, "rU")
		if opts.table is None:
			table = os.path.splitext(file)[0]
		else:
			table = opts.table

	for line in readCSV(fd):
		if opts.fields:
			fields = [x.strip() for x in opts.fields.split(",")]
			fields = "(%s)" % ",".join(fields)
		else:
			fields = ""
		values = ",".join(["\"%s\"" % x for x in line])
		print "INSERT INTO %s %s VALUES (%s);" % (table, fields, values)

if __name__ == "__main__":
	main()
