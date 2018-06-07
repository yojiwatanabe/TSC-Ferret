#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import dumpPluginOut
import processDump

parser = argparse.ArgumentParser(description = 'Helper script to retrieve \
                                 plugin output from Service Center scans')
parser.add_argument('pluginID', help = 'Plugin ID for the desired plugin output')
parser.add_argument('-i', dest= 'iFile', help = 'Input file')
args = parser.parse_args()

dumpPluginOut.dumpPluginData(args.pluginID)

if args.iFile:
    processDump.createTable(args.pluginID, args.iFile)
else:
    processDump.createTable(args.pluginID)

