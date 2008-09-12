#!/usr/bin/env python
# Filename: getlibdeps
# Module:   getlibdeps
# Date:     27th June 2005
# Author:   James Mills <prologic@shortcircuit.net.au>

"""getlibdeps

Get library dependencies of a binary file
and list required ports.

NOTE: This is a CRUX/Linux specific script.
See: http://www.crux.nu/
"""

__desc__ = "Get Library Dependancies"
__version__ = "0.0.1"
__author__ = "James Mills"
__email__ = "%s <prologic@shortcircuit.net.au>" % __author__
__url__ = "http://shortcircuit.net.au/~prologic/"
__copyright__ = "CopyRight (C) 2005 by %s" % __author__
__license__ = "GPL"

import os
import sys
from popen2 import popen4 as popen

def find_port(lib):
	stdout, stdin  = popen("prt-cache fsearch %s | grep \"Found in.*\" -o" % lib)
	ports = {}
	for line in stdout:
		port = line.strip("\t\n\r :")
		if port != "":
			head, port = os.path.split(port)
			repo = os.path.basename(head)
			if repo != "base":
				ports[port] = repo
	stdout.close()
	stdin.close()
	return ports

def find_ports(libs):
	ports = {}
	for lib in libs:
		ports.update(find_port(lib))
	return ports

def find_libs(file):
	stdout, stdin  = popen("objdump -p %s | grep NEEDED | sed -s \"s/.*NEEDED \+//\"" % file)
	libs = []
	for line in stdout:
		lib = line.strip()
		if lib != "":
			libs.append(lib)
	stdout.close()
	stdin.close()
	return libs

def main():

	file = sys.argv[1]

	if os.path.isfile(file):

		print file

		libs = find_libs(file)
		print " Libraries:"
		for lib in libs:
			print "  * %s" % lib

		print " Ports::"
		ports = find_ports(libs)
		for port, repo in ports.iteritems():
			print "  * %s (%s)" % (port, repo)

if __name__ == "__main__":
	main()
