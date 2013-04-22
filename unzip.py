#!/usr/bin/env python

import sys

from zipfile import ZipFile

ZipFile(sys.argv[1]).extractall()
