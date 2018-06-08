#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is the main driver file that the user runs. It takes command line
# arguments and calls all of the other modules. There is one positional
# argument that this file takes and one optional should follow -i

import argparse
import dumpPluginOut
import processDump
from sys import exit


parser = argparse.ArgumentParser(description = 'Helper script to retrieve \
                                 plugin output from Service Center scans')
parser.add_argument('pluginID', help = 'Plugin ID for the desired plugin output')
parser.add_argument('-i', dest= 'iFile', help = 'Input file')
args = parser.parse_args()
try:
	dumpPluginOut.dumpPluginData(args.pluginID)
	processDump.createTable(args.pluginID, args.iFile)
except Exception as e:
	print 'ERROR CODE [' + str(e.code) + ']:'
	print e.msg.encode('ascii')
	exit(e.code)

print "done"