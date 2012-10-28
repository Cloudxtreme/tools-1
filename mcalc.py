#!/usr/bin/env python

from optparse import OptionParser

__version__ = "0.1"

USAGE = "%prog <options>"
VERSION = "%prog v" + __version__

def interest(P, i, f):
    return P * i / f

def payments(P, i, f, p):
    n = 0
    I = 0.0
    while P > 0:
        a = interest(P, i, f)
        b = p - a
        P -= b
        n += 1
        I += a
        print "Month %d" % n
        print " Interest: $%0.2f" % a
        print " Payment:  $%0.2f" % b
        print " Owing:    $%0.2f" % P
    return n, I

def parse_options():
	parser = OptionParser(usage=USAGE, version=VERSION)

	parser.add_option("-i", "--interest",
			action="store", type="float", default=7.80,
            dest="i", metavar="INTEREST",
			help="Interest rate (%)")
	parser.add_option("-p", "--payments",
			action="store", type="float", default=5000.0,
            dest="p", metavar="PAYMENTS",
			help="Payments per month ($)")
	parser.add_option("-P", "--Principal",
			action="store", type="float", default=300000.0,
            dest="P", metavar="PRINCIPAL",
			help="Principal ammount ($)")
	parser.add_option("-f", "--frequency",
			action="store", type="float", default=12.0,
            dest="f", metavar="FREQUENCY",
			help="Frequency of payments")

	opts, args = parser.parse_args()

	return opts, args

def main():
    opts, args = parse_options()

    i = opts.i
    f = opts.f
    p = opts.p
    P = opts.P

    i = i / 100.0

    n, I = payments(P, i, f, p)
    t = n / f

    print "No. of payments: %d (%0.2fyrs)" % (n, t)
    print "Total Interest:  $%0.2f" % I

if __name__ == "__main__":
    main()
