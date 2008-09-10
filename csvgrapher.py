#!/usr/bin/env python

# Module:	csvgrapher
# Date:		13th June 2008
# Author:	James Mills, prologic at shortcircuit dot net dot au

"""csvgrapher

Tool to graph data in a CSV file given a field to
graph. This tool depends on csvreader for reading
and parsing the CSV file. This is useful for graphing
bank transactions or mortage balances from your bank.
"""

__desc__ = "CSV Grapher"
__version__ = "0.1"
__author__ = "James Mills"
__email__ = "%s, prologic at shortcircuit dot net dot au" % __author__
__url__ = "http://shortcircuit.net.au/~prologic/"
__copyright__ = "CopyRight (C) 2005-2008 by %s" % __author__
__license__ = "GPL"

import optparse

from pylab import plot, show

from csvreader import readCSV

USAGE = "%prog [options] <file> <field>"
VERSION = "%prog v" + __version__

def parse_options():
	"""parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.
	"""

	parser = optparse.OptionParser(usage=USAGE, version=VERSION)

	parser.add_option("-r", "--reverse",
			action="store_true", default=False, dest="reverse",
			help="Reverse the order of the data (default: False)")

	parser.add_option("-i", "--invert",
			action="store_true", default=False, dest="invert",
			help="Insert the data values (default: False)")

	opts, args = parser.parse_args()

	if len(args) < 2:
		parser.print_help()
		raise SystemExit, 1

	return opts, args

def main():
	opts, args = parse_options()

	file = args[0]
	field = int(args[1])

	if file == "-":
		fd = sys.stdin
	else:
		fd = open(file, "rU")

	data = []

	for line in readCSV(fd):
		data.append(float(line[field]))

	if opts.reverse:
		data.reverse()

	if opts.invert:
		data = [x * -1 for x in data]

	plot(data)
	show()

if __name__ == "__main__":
	main()
