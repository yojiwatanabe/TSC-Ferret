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
import pdfkit as pdf
from re import compile, search


DUMP_FILE = 'pluginText.dump'
OUTPUT_FILENAME = 'results.'
HTML_OUTPUT = OUTPUT_FILENAME + 'html'
CSV_OUTPUT = OUTPUT_FILENAME + 'csv'
PDF_OUTPUT = OUTPUT_FILENAME + 'pdf'
JSON_OUTPUT = OUTPUT_FILENAME + 'json'
HTML_DELIMITER = '<br>'
ALT_DELIMITER = ' | '
SECS_PER_WEEK = 604800
OUTPUT_TYPES = ['html', 'pdf', 'csv', 'json']
HOST_VALUES = ['IP', 'DNS', 'L_SEEN', 'REPO', 'CONTENT', 'ID', 'MAC']


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
def searchable_mode(data, input_data, result_mat, is_html):
    # Checks if the output is a CSV or HTML, takes away HTML tags if CSV output
    if ~is_html:
        delimiter = ALT_DELIMITER
    else:
        delimiter = HTML_DELIMITER
        
    for i, host in enumerate(data):
        for j, input_line in enumerate(input_data):
            temp_list = ''
            compiled_input = compile(input_line.lower())
            for line in host['CONTENT']:
                found = search(compiled_input, line.lower())
                if found:
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
#          html: Boolean value of if output format is a html file
# Output - Numpy matrix object, where each row represents a different host, and each column represents a different
#          software. This means matrix elements at row row index [i] will have software information about the host with
#          ID = i + 1. Elements along column [j] will be lists of the software on line number j + 1 in input_file.
#          E.G. if the second line of my input file is 'ssh', result_mat[0][1] will be all ssh programs installed on
#          host with ID 1.
def create_matrix(data, input_data, is_html, columns):
    if columns and 'content' not in map(lambda x: x.lower(), columns):
        return

    if input_data:
        result_mat = np.empty((len(data), len(input_data)), dtype=object)
    else:
        result_mat = np.empty((len(data), 1), dtype=object)
    if input_data:
        result_mat = searchable_mode(data, input_data, result_mat, is_html)
    else:
        for i, host in enumerate(data):
            temp_string = ''
            for line in host['CONTENT']:
                temp_string += line

                # Skips adding new line HTML tag if output is an HTML file
                if is_html:
                    temp_string += HTML_DELIMITER

            temp_string = temp_string.replace(u'<plugin_output>', u'')
            temp_string = temp_string.replace(u'</plugin_output>', u'')
            result_mat[i] = temp_string

    return result_mat


# 		dead_host_info()
#
# Returns information about a single host to be . Helper function to get_host_info
# Input  - host_data: Dictionary array with host info like DNS, IP, and REPO
#          delimiter: Delimiter to use between points of information, will change depending on if the output type is CSV
# Output - String array with all of the hosts' information
def dead_host_info(host, delimiter, columns):
    # Checks if output will be to CSV or HTML, adjusts start/end of host info field accordingly
    if delimiter != ALT_DELIMITER:
        font_start = '<font style="color:#DF0101">'
        font_end = '</font>'
    else:
        font_start = ''
        font_end = ''

        if columns:
            temp = specific_host_columns(host, columns)
            return temp

    temp = (font_start
            + 'HOST NOT SEEN IN ' + str(round((time.time() - float(host['L_SEEN'])) / SECS_PER_WEEK, 2)) + ' WEEKS'
            + delimiter + 'DNS: ' + host['DNS']
            + delimiter + 'IP: ' + host['IP']
            + delimiter + 'Repository: ' + host['REPO']
            + delimiter + 'MAC Address: ' + host['MAC']
            + delimiter + 'Last seen: ' + time.ctime(float(host['L_SEEN']))
            + font_end).encode('utf-8')
    return temp


#       specific_host_columns()
#
# Returns information on the host given column arguments. Returns only the host information requested. Helper function
# to get_host_info().
# Input  - host: dictionary with host info
#        - columns: string array with columns to be returned
# Output - string with the host information to be saved
def specific_host_columns(host, columns):
    temp = []
    for value in columns:
        if value.lower() == 'content':
            continue

        if value.strip().upper() in HOST_VALUES:
            temp.append(host[value.strip().upper()])

    return temp


# 		get_host_info()
#
# Returns information on the host in a pd.to_html friendly format (string)
# Input  - host_data: Dictionary array with host info like DNS, IP, and REPO
#          csv: Boolean value of if output format is a CSV file
# Output - String array with all of the hosts' information
def get_host_info(host_data, html, columns=''):
    # Checks if the output is HTML, takes away HTML tags if not, uses alternative delimiter
    if not html:
        delimiter = ALT_DELIMITER
    else:
        delimiter = HTML_DELIMITER

    host_info = []
    for host in host_data:
        # Edge case for a likely dead machine
        if (time.time() - float(host['L_SEEN']) > SECS_PER_WEEK) & (not columns):
            temp = dead_host_info(host, delimiter, columns)
            host_info.append(temp)
            continue

        if columns:
            temp = specific_host_columns(host, columns)
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
    if data is None:
        return

    if input_data:
        data_frame = pd.DataFrame(data, index=range(1, len(data) + 1), columns=input_data)
    else:
        data_frame = pd.DataFrame(data, index=range(1, len(data) + 1), columns=['PLUGIN OUTPUT:'])

    return data_frame


#       no_data()
#
# Helper function used by make_host_frame() in case no host columns were specified in a columns argument. Checks if the
# given list is empty, meaning specific_host_columns() has not saved any columns specific to the host.
# Input  - to_check: the list of host information to
# Output -
def no_data(to_check):
    if to_check is None:
        return True
    elif to_check[0] is not None:
        return False

    return True


# 		make_host_frame()
#
# Creates the pandas data frame to be converted into an HTML table. Sets up layout according to type of query
# Input  - data: Numpy matrix with information to be listed in table
#          input_data: list of strings that were queried in the plugin output
# Output - String array with all of the hosts' information
def make_host_frame(data, columns):
    if columns and no_data(data):
        return
    elif columns:
        columns_upper = list(set(i.upper() for i in columns))
        if 'CONTENT' in columns_upper:
            columns_upper.remove('CONTENT')
            host_frame = pd.DataFrame(data, index=range(1, len(data) + 1), columns=columns_upper)
        else:
            host_frame = pd.DataFrame(data, index=range(1, len(data) + 1), columns=columns_upper)

    else:
        host_frame = pd.DataFrame(data, index=range(1, len(data) + 1), columns=['Host Info:'])
    return host_frame


# 		write_to_html()
#
# Writes the given numpy matrix to a table in a HTML file
# Input  - data: Plugin output data, pre-processed according to user input (search, repository/host filters)
#          input_data: List of programs to search for (if any)
#          host_data: List with host information
# Output - none, out to file
def write_to_html(data, input_data, host_data, columns):
    host_frame = make_host_frame(host_data, columns)
    data_frame = make_data_frame(data, input_data)

    pd.set_option('display.max_colwidth', -1)
    full_frame = pd.concat([host_frame, data_frame], axis=1)

    full_frame.to_html(HTML_OUTPUT, escape=False)

    return


# 		write_to_csv()
#
# Writes the given numpy matrix to a CSV file
# Input  - data: Plugin output data, pre-processed according to user input (search, repository/host filters)
#          input_data: List of programs to search for (if any)
#          host_data: List with host information
# Output - none, out to file
def write_to_csv(data, input_data, host_data, columns):
    host_frame = make_host_frame(host_data, columns)
    data_frame = make_data_frame(data, input_data)

    full_frame = pd.concat([host_frame, data_frame], axis=1)
    full_frame.to_csv(CSV_OUTPUT)

    return


# 		write_to_pdf()
#
# Writes the given numpy matrix to a PDF file
# Input  - data: Plugin output data, pre-processed according to user input (search, repository/host filters)
#          input_data: List of programs to search for (if any)
#          host_data: List with host information
# Output - none, out to file
def write_to_pdf(data, input_data, host_data, columns):
    write_to_html(data, input_data, host_data, columns)
    options = {
        'page-size': 'A4',
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        'dpi': 225
    }
    pdf.from_file(HTML_OUTPUT, PDF_OUTPUT, options=options)

    return


# 		write_to_json()
#
# Writes the given numpy matrix to a PDF file
# Input  - data: Installed program information about each requested program. m rows by n columns, where each row is a
#                host, and each column is a program that was specified to search for
#          input_data: List of programs to search for
#          host_data: List with host information
# Output - none, out to file
def write_to_json(data, input_data, host_data, columns):
    host_frame = make_host_frame(host_data, columns)
    data_frame = make_data_frame(data, input_data)

    full_frame = pd.concat([host_frame, data_frame], axis=1)
    full_frame.to_json(JSON_OUTPUT)

    return


# 		create_table()
#
# Drives the processDump module. Loads data, processes it as necessary, and converts it to an HTML table, and writes out
# to a file 'results.html'.
# Input  - output_type: string containing the format in which to output results (csv, html, json, pdf)
#          infile: Special query modifier, optional argument. See README for more
# Output - none, out to file
def create_table(output_type, columns='', infile=''):
    data = load_data()
    input_data = ''

    if infile:
        input_data = read_input(infile)

    is_html = (output_type == 'html')
    result_mat = create_matrix(data, input_data, is_html, columns)
    host_info = get_host_info(data, is_html, columns)

    output_functions = {0: write_to_html,
                        1: write_to_pdf,
                        2: write_to_csv,
                        3: write_to_json}

    # Call on correct function according to output type
    output_functions[OUTPUT_TYPES.index(output_type)](result_mat, input_data, host_info, columns)

    return
