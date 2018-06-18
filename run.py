#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is the main driver file that the user runs. It takes command line
# arguments and calls all of the other modules. There is one positional
# argument that this file takes and one optional should follow -i

import argparse
import dump_plugin_output
import process_dump
from sys import exit


#       initiate_argparse()
#
# Function that initializes the argument parser, adding the necessary runtime arguments and parsing the user input
# Input  - none
# Output - argparse Argument Parser object
def initiate_argparse():
    parser = argparse.ArgumentParser(description='Helper script to retrieve plugin output from Service Center scans')
    parser.add_argument('plugin_id', help='Plugin ID for the desired plugin output')
    parser.add_argument('-s', '--search_queries', dest='search_list', help='Input file for words to query output '
                                                                           '(e.g. -s queries.txt)')
    parser.add_argument('-R', '--repo_list', dest='repos', help='Input file for repositories to query '
                                                                '(e.g. -R repos.txt)')
    parser.add_argument('-H', '--host_list', dest='hosts', help='Input file for hosts to query '
                                                                '(e.g. -H hosts.txt)')
    parser.add_argument('-i', '--ip_range', dest='ip_range', help='Range of IPs from which to gather data '
                                                                  '(e.g. --ip_range 127.0.0.1-192.168.0.1)')
    parser.add_argument('-c', '--csv_out', dest='csv', help='Change from default html output to a CSV output',
                        default=False, action='store_true')
    parser.add_argument('-d', '--allow_duplicates', dest='duplicates', help='Change from default behavior of only '
                        'outputting latest scan results to show all results', default=False, action='store_true')

    return parser.parse_args()


def main():
    args = initiate_argparse()

    try:
        dump_plugin_output.dump_plugin_data(args.plugin_id, args.repos, args.hosts, args.ip_range, args.duplicates)
        process_dump.create_table(args.csv, args.search_list)
    except (Exception, KeyboardInterrupt) as e:
        print '\n###### ERROR'
        print 'Exception: [' + str(e) + ']:'
        exit(1)

    if args.csv:
        print "Created " + process_dump.CSV_OUTPUT
    else:
        print "Created " + process_dump.HTML_OUTPUT

    return 0


# # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    main()
