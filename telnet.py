#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=3 sts=3 ts=3

import optparse

from pymills.io import Stdin
from pymills.net.sockets import TCPClient
from pymills import __version__ as systemVersion
from pymills.event import listener, Manager, Debugger, UnhandledEvent

USAGE = "%prog [options] <host> [<port>]>"
VERSION = "%prog v" + systemVersion

###
### Functions
###

def parse_options():
	"""parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.
	"""

	parser = optparse.OptionParser(usage=USAGE, version=VERSION)

	parser.add_option("-s", "--ssl",
			action="store_true", default=False, dest="ssl",
			help="Enable Secure Socket Layer (SSL)")
	parser.add_option("-d", "--debug",
			action="store_true", default=False, dest="debug",
			help="Enable debug mode. (Default: False)")

	opts, args = parser.parse_args()

	if len(args) < 1:
		parser.print_help()
		raise SystemExit, 1

	return opts, args

###
### Components
###

class Telnet(TCPClient):

	@listener("connect")
	def onCONNECT(self, host, port):
		print "Connected to %s" % host

	@listener("read")
	def onREAD(self, data):
		print data.strip()

	@listener("stdin:read")
	def onINPUT(self, data):
		self.write(data)

###
### Main
###

def main():
	opts, args = parse_options()

	host = args[0]
	if len(args) > 1:
		port = int(args[1])
	else:
		port = 23

	e = Manager()
	stdin = Stdin(e)

	if opts.debug:
		debugger = Debugger(e)
		debugger.IgnoreEvents.extend(["Read", "Write"])

	telnet = Telnet(e)

	print "Trying %s..." % host
	telnet.open(host, port, ssl=opts.ssl)

	while telnet.connected:
		try:
			e.flush()
			stdin.poll()
			telnet.poll()
		except KeyboardInterrupt:
			break
	telnet.close()

###
### Entry Point
###

if __name__ == "__main__":
	main()
