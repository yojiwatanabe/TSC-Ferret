#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is the main driver file that the user runs. It takes command line
# arguments and calls all of the other modules. There is one positional
# argument that this file takes and one optional should follow -i

import argparse
import dumpPluginOut
import processDump
from sys import exit


def initiateArgParse():
    parser = argparse.ArgumentParser(description='Helper script to retrieve plugin output from Service Center scans')
    parser.add_argument('pluginID', help='Plugin ID for the desired plugin output')
    parser.add_argument('-i', dest='search_list', help='Input file for words to query output')
    parser.add_argument('-R', dest='repo_list', help='Input file for repositories to query')
    parser.add_argument('-H', dest='host_list', help='Input file for hosts to query')

    return parser.parse_args()


def main():
    args = initiateArgParse()

    try:
        dumpPluginOut.dumpPluginData(args.pluginID)
        processDump.createTable(args.pluginID, args.iFile)
    except Exception as e:
        print 'ERROR CODE [' + str(e.code) + ']:'
        print e.msg.encode('ascii')
        exit(e.code)

    print "done"


# # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    main()
