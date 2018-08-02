#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is the main driver file that the user runs. It takes command line
# arguments and calls all of the other modules. There is one positional
# argument that this file takes and one optional should follow -i

import json
import argparse
import process_dump
import email_results
import dump_plugin_output
from sys import exit
from base64 import b64decode

ASCII_ART = """             .,..,.,
         .***//***/(//((/           _________   ______     ______
           *,**,//((//(( .*.,      |  _   _  |.' ____ \  .' ___  |
      .,,./.,,****/***.,(((/,      |_/ | | \_|| (___ \_|/ .'   \_|
     ..,* .   , ,  .     ,/(/,,        | |     _.____`. | |
     .,,.                 ./#,.       _| |_   | \____) |\ `.___.'\\
      .       .   .   .,/*,./*,.     |_____|   \______.' `.____ .'
          *(//.**,.,/(/%%%*,,,.     ________                               _
         .*#&(**((*/#%&@&&%,.*.    |_   __  |                             / |_
  ,...   ,*//,*//*/%%%%%%*,/         | |_ \_|.---.  _ .--.  _ .--.  .---.`| |-'
  *,*,,. ,/(*     ,,*/*/%&%./.       |  _|  / /__\\\\[ `/'`\][ `/'`\]/ /__\\\\| |
 ./****,  .*      ..,*/,(((##(.     _| |_   | \__., | |     | |    | \__.,| |,
./***/(*(,.       ../...*%%%%%(*   |_____|   '.__.'[___]   [___]    '.__.'\__/
,//*/(/(((//,.     ..,*%/%%&&&%(#,,,..  ..
.///((##(##(##(%&&&&%%%%&&&&&&&&%%##%%%%%%#/,
.(((((###/%%#%%&%#&%&&%&&&&@&&&&%%%#%%%%&&%%%#/.
.((###%%##%%%%%&&&&&%%&&&@@&&&&&%%%#&&&&&&&&&%#*
./#(#%%%#%%%%&&&&&&&&&&&&&@@@@@&&&%%%%%%&&&&&&&&%#/.
 (#%%%%%%%%%&&&&&&@&@&&&&@@@@@@@&&%%%%%&&&&&&&&&&&%/.
,##%%%&&&&&&&&&&&&&&@@&@@@@@@@@@@&%%%%%%&&&&&&&&&&&&%/,,,.,,...
,#%%%%%&&&&&&&&&@@@@@@@@@@@@@@@@@&%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&%%#(*,.
*%%%%%&&&&&&@&@@@@@@@@@@@@@@@@@@@&&%%&&&&&&&@@@@@&&&&&@@@@@@@@@@@&&@&&&&&%*
,#%%&&&&&@&@@@@@@@&@@@@@@@@@@@@@@@&&%%&&&&&&@@@@@@&@@@@@@@@@@@@@@@@@@@@&&&%,
 /%%&&&@&@@&@@@@@@@@@@@@@@@@@@@@@@@&%&&&&&&&&&&&&&&@@@@@@@@@@@@@@@@@@@@@@@@&(
  (%&&&@@@@@@&@@@&&@@@@@@&@@@@@@@@@&&&&&&&&&&&&&&&&&&&@@@@@@@@@@@@@@@&@&@@@&/
  ,%%&&@@@@@@@@@@&&&@@@@@@@@@@@@@@@@&&&&&&&&&&&&&%%##((///**////(#&@@@@@@@@&/.
  *%&@@@@@@/*(%&&@@&@@@@@&&@@@@@@@@@@@@@&&%%##((//**,...         ..,,(&@@@/.
  %&@@@&@@&//(#%&&&&@@@@@&&@@@@@@@&&&&&%%%%%%###((//
  /&&(,@%,@&(#////#&@@@@&@@&&@%&&%###((//**,,,.
                  /#&/@@@*@@&&%&&%(*.
"""


#       initiate_argparse()
#
# Function that initializes the argument parser, adding the necessary runtime arguments and parsing the user input
# Input  - none
# Output - argparse Argument Parser object
def initiate_argparse():
    parser = argparse.ArgumentParser(description='Helper script to retrieve plugin output from Security Center scans')
    plugin_source = parser.add_mutually_exclusive_group(required=True)

    plugin_source.add_argument('-P', '--plugin_id', dest='plugin_id', help='Plugin ID for the desired plugin output')
    plugin_source.add_argument('-C', '--config', dest='config', help='Config file to load credentials and arguments')

    parser.add_argument('-s', '--search_queries', dest='search_list', help='Input file for words to query output '
                                                                           '(e.g. -s queries.txt)')
    parser.add_argument('-R', '--repo_list', dest='repos', help='Input file for repositories to query '
                                                                '(e.g. -R repos.txt)')
    parser.add_argument('-H', '--host_list', dest='hosts', help='Input file for hosts to query '
                                                                '(e.g. -H hosts.txt)')
    parser.add_argument('-i', '--ip_range', dest='ip_range', help='Range of IPs from which to gather data '
                                                                  '(e.g. --ip_range 127.0.0.1-192.168.0.1)')
    parser.add_argument('-d', '--allow_duplicates', dest='duplicates', help='Change from default behavior of only '
                        'outputting latest scan results to show all results', default=False, action='store_true')
    parser.add_argument('-e', '--email_results', dest='email_results', help='Email results of TSC Ferret to the given '
                        'recipients', default=False, action='store_true')
    parser.add_argument('-o', '--output_type', dest='output', help='Change from default html output to a csv, pdf,'
                        ' or json file', default='html')
    parser.add_argument('-c', '--columns', dest='columns', help='Specify data columns to be included in the output. '
                                                                'Currently supports \'IP\', \'DNS\', \'Repository\', '
                                                                '\'MAC\', \'L_SEEN\'')

    return parser.parse_args()


#   check_valid_output_type()
#
# Ensures that the output file type specified by the user is supported by TSC Ferret
# Input  - file_type: string containing the file type specified
# Output - none, will exit if unsupported
def check_valid_output_type(file_type):
    if file_type.lower() not in process_dump.OUTPUT_TYPES:
        print('Unsupported file type!\nSupported file types: %s' % ', '.join(process_dump.OUTPUT_TYPES))
        exit(1)

    return


def main():
    args = initiate_argparse()
    print ASCII_ART

    try:
        if args.config:
            f = open(args.config, 'r')
            config = json.load(f)

            out_file_type = config['output']
            to_email = config['email_results']
            columns = config['columns']
            if columns:
                columns = columns.split(',')
                temp_columns = []
                for value in columns:
                    value = value.strip()
                    if value.upper() not in process_dump.HOST_VALUES:
                        print value + " column does not exist"
                        continue
                    temp_columns.append(value)
                columns = temp_columns
                if not columns:
                    print "None of the specified columns exists. Showing all data instead"


            dump_plugin_output.dump_plugin_data(config['plugin_id'], config['repo_list'], config['host_list'],
                                                config['ip_range'], config['duplicates'], config['user'],
                                                b64decode(config['pass']))
            process_dump.create_table(out_file_type, columns, config['search_list'])
        else:
            out_file_type = args.output
            to_email = args.email_results
            columns = args.columns
            if columns:
                columns = columns.split(',')
                temp_columns = []
                for value in columns:
                    value = value.strip()
                    if value.upper() not in process_dump.HOST_VALUES:
                        print value + " column does not exist"
                        continue
                    temp_columns.append(value)
                columns = temp_columns
                if not columns:
                    print "None of the specified columns exists. Showing all data instead"

            dump_plugin_output.dump_plugin_data(args.plugin_id, args.repos, args.hosts, args.ip_range, args.duplicates,
                                                '', '')
            process_dump.create_table(out_file_type, columns, args.search_list)

        if to_email:
            if args.config:
                email_results.craft_and_send_message(config['plugin_id'], config['host_list'], config['repo_list'],
                                                     config['ip_range'], config['search_list'], config['duplicates'],
                                                     out_file_type)
            else:
                email_results.craft_and_send_message(args.plugin_id, args.hosts, args.repos, args.ip_range,
                                                     args.search_list, args.duplicates, out_file_type)

    except Exception as e:
        print '\n###### ERROR'
        print 'Exception: [' + str(e) + ']:'
        exit(1)

    except KeyboardInterrupt:
        print '\n###### Keyboard Interrupt'
        print 'exiting...'
        exit(1)        

    print "Done."

    return 0


# # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    main()
