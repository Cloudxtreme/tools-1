#!/usr/bin/env python

from optparse import OptionParser

__version__ = "0.1"

USAGE = "%prog <options>"
VERSION = "%prog v" + __version__

def interest(P, i, f):
    return P * i / f

def payments(P, i, f, p, s, q):
    n = 0
    I = 0.0
    while P > 0:
        a = interest(P, i, f)
        b = p - a
        P -= b
        n += 1
        I += a
        if not q:
            print "Iteration %d" % n
            print " Interest: $%0.2f" % a
            print " Payment:  $%0.2f" % b
            print " Owing:    $%0.2f" % P

        if s and n >= s:
            break

    return n, I, P

def parse_options():
	parser = OptionParser(usage=USAGE, version=VERSION)

	parser.add_option("-i", "--interest",
			action="store", type="float", default=7.80,
            dest="i", metavar="INTEREST",
			help="Interest rate (%)")
	parser.add_option("-p", "--payments",
			action="store", type="float", default=5000.0,
            dest="p", metavar="PAYMENTS",
			help="Payments per iteration ($)")
	parser.add_option("-P", "--Principal",
			action="store", type="float", default=300000.0,
            dest="P", metavar="PRINCIPAL",
			help="Principal ammount ($)")
	parser.add_option("-f", "--frequency",
			action="store", type="float", default=12.0,
            dest="f", metavar="FREQUENCY",
			help="Frequency of payments")
	parser.add_option("-s", "--stop",
			action="store", type="int", default=0,
            dest="s", metavar="STOP",
			help="Stop after n iterations")
	parser.add_option("-q", "--quiet",
			action="store_true", default=False,
            dest="q",
			help="Enable quiet mode")

	opts, args = parser.parse_args()

	return opts, args

def main():
    opts, args = parse_options()

    q = opts.q
    s = opts.s
    i = opts.i
    f = opts.f
    p = opts.p
    P = opts.P

    i = i / 100.0

    n, I, B = payments(P, i, f, p, s, q)
    t = n / f

    print "Payments: %d (%0.2fyrs)" % (n, t)
    print "Balance:  $%0.2f" % B
    print "Interest: $%0.2f" % I

if __name__ == "__main__":
    main()
