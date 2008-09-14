#!/usr/bin/env python

# Module:	csvanalysis
# Date:		14th September 2008
# Author:	James Mills, prologic at shortcircuit dot net dot au

"""csvanalysis

Tool to read CSV data files and analysis their data
and their fields. The resulting output will help
a developer or database administrator to determine
the best way to store this data.
"""

__desc__ = "CSV Analysis Tool"
__version__ = "0.1"
__author__ = "James Mills"
__email__ = "%s, prologic at shortcircuit dot net dot au" % __author__
__url__ = "http://shortcircuit.net.au/~prologic/"
__copyright__ = "CopyRight (C) 2005-2008 by %s" % __author__
__license__ = "GPL"

import csv
import optparse
from cStringIO import StringIO

from pymills.db import Record
from pymills.table import Table, Header, Row, Cell

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

def analyzeCSV(data):
	d = {"Rows": 0, "Columns": 0, "Fields": {}}
	fields = d["Fields"]
	for row in data:
		d["Rows"] += 1
		for i, col in enumerate(row):
			field = fields.get(i, {})

			fmin = field.get("min", None)
			favg = field.get("avg", None)
			fmax = field.get("max", None)
			total = field.get("total", 0)

			l = len(col)
			total += l
			field["total"] = total

			if fmin is None:
				fmin = l
			else:
				if l < fmin:
					fmin = l
			if favg is None:
				favg = l
			else:
				favg = float(total) / float(d["Rows"])
				
			if fmax is None:
				fmax = l
			else:
				if l > fmax:
					fmax = l

			field["min"] = fmin
			field["avg"] = favg
			field["max"] = fmax

			del field["total"]
			fields[i] = field
	else:
		d["Columns"] = len(row)

	records = []
	for k, v in fields.iteritems():
		records.append(Record(v.items()))

	x = records[0]
	headers = []
	for k, v in x.iteritems():
		headers.append(Header(k,
			align="left",
			width=max(
				max([len(str(x[k])) for x in records]) + 2,
				len(k) + 2)))
	rows = []
	for record in records:
		rows.append(Row([Cell(x) for x in record.values()]))
	table = Table(headers, rows)
	table.refresh()

	print table

def main():
	opts, args = parse_options()

	file = args[0]

	if file == "-":
		fd = sys.stdin
	else:
		fd = open(file, "rU")

	analyzeCSV(readCSV(fd))

if __name__ == "__main__":
	main()
