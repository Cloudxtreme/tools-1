#!/usr/bin/env python

import optparse

from pymills.event import *
from pymills import __version__ as systemVersion
from pymills.net.sockets import TCPServer, TCPClient

USAGE = "%prog [options] host[:port]"
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

	parser.add_option("-b", "--bind",
			action="store", type="str", default="0.0.0.0", dest="bind",
			help="Bind to address:[port] (UDP) (test remote events)")
	parser.add_option("-s", "--ssl",
			action="store_true", default=False, dest="ssl",
			help="Enable Secure Socket Layer (SSL)")
	parser.add_option("-d", "--debug",
			action="store_true", default=False, dest="debug",
			help="Enable debug mode. (Default: False)")

	opts, args = parser.parse_args()

	if not args:
		parser.print_help()
		raise SystemExit, 1
	
	return opts, args

###
### Events
###

class ClientOpen(Event): pass
class ClientData(Event): pass
class ClientClosed(Event): pass
class TargetData(Event): pass
class TargetClosed(Event): pass

###
### Components
###

class Server(TCPServer):

	channel = "server"
	client = None

	@listener("connect")
	def onCONNECT(self, sock, host, port):
		self.client = sock
		self.push(ClientOpen(), "target:open")

	@listener("disconnect")
	def onDISCONNECT(self, sock):
		self.client = None
		self.push(ClientClosed(), "target:closed")

	@listener("read")
	def onREAD(self, sock, data):
		self.push(ClientData(data), "target:data")

	@listener("closed")
	def onCLOSED(self):
		if self.client:
			self.close(self.client)

	@listener("data")
	def onDATA(self, data):
		self.write(self.client, data)

class Target(TCPClient):

	channel = "target"

	connect = None

	@listener("open")
	def onOPEN(self):
		self.open(*self.connect)
	
	@listener("data")
	def onDATA(self, data):
		self.write(data)

	@listener("closed")
	def onCLOSED(self):
		self.close()

	@listener("read")
	def onREAD(self, data):
		self.push(TargetData(data), "server:data")

	@listener("disconnect")
	def onDISCONNECT(self):
		self.push(TargetClosed(), "server:closed")

###
### Main
###

def main():
	opts, args = parse_options()

	if ":" in opts.bind:
		address, port = opts.bind.split(":")
		port = int(port)
		bind = (address, port)
	else:
		bind = (opts.bind, 8000)

	if ":" in args[0]:
		address, port = args[0].split(":")
		port = int(port)
		connect = (address, port)
	else:
		connect = (args[0], 8000)

	debugger.set(opts.debug)

	server = Server(e, address=bind[0], port=bind[1])
	target = Target(e)
	target.connect = connect

	while True:
		try:
			e.flush()
			server.poll()
			if target.connected:
				target.poll()
		except UnhandledEvent:
			pass
		except KeyboardInterrupt:
			target.close()
			server.close()
			break

###
### Entry Point
###

if __name__ == "__main__":
	main()
