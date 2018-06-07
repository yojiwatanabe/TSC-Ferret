#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import dumpPluginOut
import processDump

parser = argparse.ArgumentParser(description = 'Helper script to retrieve \
                                 plugin output from Service Center scans')
parser.add_argument('pluginID', help = 'Plugin ID for the desired plugin output')
args = parser.parse_args()

dumpPluginOut.dumpPluginData(args.pluginID)
processDump.createTable()