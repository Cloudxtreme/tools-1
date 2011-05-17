#!/usr/bin/env python

from optparse import OptionParser

__version__ = "0.1"

USAGE = "%prog <options> high low"
VERSION = "%prog v" + __version__

def shares(c, p):
    return c / p

def margin(h, l):
    return (h - l) / h

def even(h, l):
    m = margin(h, l)

    return (39.90 * h) / (h - l)

def parse_options():
    parser = OptionParser(usage=USAGE, version=VERSION)

    opts, args = parser.parse_args()

    if len(args) < 2:
        parser.print_help()
        raise SystemExit, 1

    return opts, args

def main():
    opts, args = parse_options()

    h = float(args[0])
    l = float(args[1])

    print "$+/-:   %0.02f" % (h - l)
    print "Margin: %0.02f%%" % (margin(h, l) * 100.0)
    print
    print "Break Event with: "
    print " Capital:         $%0.2f" % even(h, l)
    print " No. Shares:      %d" % (shares(even(h, l), l) + 1)
    print

    for i in [100, 200, 500, 1000]:
        cost = (shares(even(h, l), l) + 1 + i) * l
        profit = (cost / l * h) - cost - 39.90
        print "Profit at +%d shares ($%0.2f): $%0.2f" % (i, cost, profit)

if __name__ == "__main__":
    main()
