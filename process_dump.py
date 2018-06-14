#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
processDump.py
This module reads in the file created by dumpPluginOut.py and creates a usable matrix out of the data after searching
for the queried data or without searching. This matrix is then used to create a html table and is written to a html
file. For searching this file reads a file given by the user and makes one query out of a line from the file. Then it
compares the list with the data output from processDump.py and gives us relevant data
"""


import json
import time
import numpy as np
import pandas as pd


DUMP_FILE = 'pluginText.dump'
HTML_OUTPUT = 'results.html'
HTML_DELIMITER = '<br>'
CSV_OUTPUT = 'results.csv'
CSV_DELIMITER = ' | '
SECS_PER_WEEK = 604800


# 		load_data()
#
# Function to load JSON information from a file stream
# Input  - none
# Output - Python dictionary with data
def load_data():
    f = open(DUMP_FILE, 'r')
    raw_data = json.load(f)
    f.close()
    return raw_data


# 		read_input()
#
# Function to load JSON information from a file stream
# Input  - none
# Output - Python dictionary with data
def read_input(infile):
    f = open(infile, 'r')
    data = f.read().splitlines()
    return data


#       searchableMode()
#
# Function to search through the plugin output data for the user-supplied queries.
# Input  - data : string list of plugin output data to search through
#          input_data : string list of queries to look for in plugin data
#          result_mat : numpy matrix where matching queries will be store
#          csv: Boolean value of if output format is a CSV filed
# Output - numpy matrix with matching queries
def searchable_mode(data, input_data, result_mat, csv):
    # Checks if the output is a CSV or HTML, takes away HTML tags if CSV output
    if csv:
        delimiter = CSV_DELIMITER
    else:
        delimiter = HTML_DELIMITER

    for i, host in enumerate(data):
        for j, input_line in enumerate(input_data):
            temp_list = ''
            for line in host['CONTENT']:
                if input_line.lower() in line.lower():
                    temp_list += line + delimiter
            if temp_list == '':
                temp_list = 'Query \'' + input_line + '\' not found'
            result_mat[i][j] = temp_list

    return result_mat


# 		create_matrix()
#
# Creates and populates a table containing software information about desired software from given hosts
# Input  - data: Host data dict object, dict with host IP, DNS, Repository, and Content
#          input_data: List of programs to search for (optional for special query)
#          csv: Boolean value of if output format is a CSV file
# Output - Numpy matrix object, where each row represents a different host, and each column represents a different
#          software. This means matrix elements at row row index [i] will have software information about the host with
#          ID = i + 1. Elements along column [j] will be lists of the software on line number j + 1 in input_file.
#          E.G. if the second line of my input file is 'ssh', result_mat[0][1] will be all ssh programs installed on
#          host with ID 1.
def create_matrix(data, input_data, csv):
    if input_data:
        result_mat = np.empty((len(data), len(input_data)), dtype=object)
    else:
        result_mat = np.empty((len(data), 1), dtype=object)
    if input_data:
        result_mat = searchable_mode(data, input_data, result_mat, csv)
    else:
        for i, host in enumerate(data):
            temp_list = ''
            for program in host['CONTENT']:
                temp_list += program
                # Skips adding new line HTML tag if output is an HTML file
                if csv:
                    continue

                temp_list += HTML_DELIMITER
            result_mat[i] = temp_list
    return result_mat


# 		dead_host_info()
#
# Returns information about a single host to be . Helper function to get_host_info
# Input  - host_data: Dictionary array with host info like DNS, IP, and REPO
#          delimiter: Delimiter to use between points of information, will change depending on if the output type is CSV
# Output - String array with all of the hosts' information
def dead_host_info(host, delimiter):
    # Checks if output will be to CSV or HTML, adjusts start/end of host info field accordingly
    if delimiter != CSV_DELIMITER:
        font_start = '<font style="color:#DF0101">'
        font_end = '</font>'
    else:
        font_start = ''
        font_end = ''

    temp = (font_start
            + 'HOST NOT SEEN IN ' + str(round((time.time() - float(host['L_SEEN'])) / SECS_PER_WEEK, 2)) + ' WEEKS'
            + delimiter + 'DNS: ' + host['DNS']
            + delimiter + 'IP: ' + host['IP']
            + delimiter + 'Repository: ' + host['REPO']
            + delimiter + 'MAC Address: ' + host['MAC']
            + delimiter + 'Last seen: ' + time.ctime(float(host['L_SEEN']))
            + font_end).encode('utf-8')
    return temp


# 		get_host_info()
#
# Returns information from the host in a pd.to_html friendly format (string)
# Input  - host_data: Dictionary array with host info like DNS, IP, and REPO
#          csv: Boolean value of if output format is a CSV file
# Output - String array with all of the hosts' information
def get_host_info(host_data, csv):
    # Checks if the output is a CSV or HTML, takes away HTML tags if CSV output, uses other delimiter
    if csv:
        delimiter = CSV_DELIMITER
    else:
        delimiter = HTML_DELIMITER

    host_info = []
    for host in host_data:
        # Edge case for a likely dead machine
        if time.time() - float(host['L_SEEN']) > SECS_PER_WEEK:
            temp = dead_host_info(host, delimiter)
            host_info.append(temp)
            continue

        temp = ('DNS: ' + host['DNS']
                + delimiter + 'IP: ' + host['IP']
                + delimiter + 'Repository: ' + host['REPO']
                + delimiter + 'MAC Address: ' + host['MAC']
                + delimiter + 'Last seen: ' + time.ctime(float(host['L_SEEN']))).encode('utf-8')
        host_info.append(temp)

    return host_info


# 		make_data_frame()
#
# Creates the pandas data frame to be converted into an HTML table. Sets up layout according to type of query
# Input  - data: Numpy matrix with information to be listed in table
#          input_data: list of strings that were queried in the plugin output
# Output - String array with all of the hosts' information
def make_data_frame(data, input_data):
    if input_data:
        data_frame = pd.DataFrame(data, index=range(1, len(data) + 1), columns=input_data)
    else:
        data_frame = pd.DataFrame(data, index=range(1, len(data) + 1), columns=['Plugin Output:'])

    return data_frame


# 		write_to_html()
#
# Writes the given numpy matrix to a table in a HTML file
# Input  - data: Installed program information about each requested program. m rows by n columns, where each row is a
#                host, and each column is a program that was specified to search for
#          input_data: List of programs to search for
#          host_data: List with host information
# Output - none, out to file
def write_to_html(data, input_data, host_data):
    host_frame = pd.DataFrame(host_data, index=range(1, len(data) + 1), columns=['Host Info:'])
    data_frame = make_data_frame(data, input_data)

    full_frame = pd.concat([host_frame, data_frame], axis=1)
    pd.set_option('display.max_colwidth', -1)
    full_frame.to_html(HTML_OUTPUT, escape=False)

    return


# 		write_to_csv()
#
# Writes the given numpy matrix to a CSV file
# Input  - data: Installed program information about each requested program. m rows by n columns, where each row is a
#                host, and each column is a program that was specified to search for
#          input_data: List of programs to search for
#          host_data: List with host information
# Output - none, out to file
def write_to_csv(data, input_data, host_data):
    host_frame = pd.DataFrame(host_data, index=range(1, len(data) + 1), columns=['Host Info:'])
    data_frame = make_data_frame(data, input_data)

    full_frame = pd.concat([host_frame, data_frame], axis=1)
    full_frame.to_csv(CSV_OUTPUT)


    return


# 		create_table()
#
# Drives the processDump module. Loads data, processes it as necessary, and converts it to an HTML table, and writes out
# to a file 'results.html'.
# Input  - infile: Special query modifier, optional argument. See README for more
#          csv: Boolean value of if output format is a CSV file
# Output - none, out to file
def create_table(infile='', csv):
    data = load_data()
    input_data = ''

    if infile:
        input_data = read_input(infile)
    result_mat = create_matrix(data, input_data, csv)
    host_info = get_host_info(data, csv)

    if csv:
        write_to_csv(result_mat, input_data, host_info)
    else:
        write_to_html(result_mat, input_data, host_info)

    return
