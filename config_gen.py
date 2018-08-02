#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
config_gen.py
This is an independent module that creates config files based on the user's
choices. The user enters the credentials and the choices of arguments which
is processed by this module and written to a file in json format
"""

import json
from base64 import b64encode
import getpass

# List of accepted file type
accepted_types = ['html', 'pdf', 'csv', 'json']
output_type = ''

# Ask the user for the required information
print 'Enter the following mandatory information:'
config_file = raw_input('Enter the name of the config file: ')
user = raw_input('Username: ')

# Get the password and convert to base64 instead of saving as plaintext
passwd = b64encode(getpass.getpass())
plugin_id = raw_input('Plugin ID: ')

# Get and validate file type
while output_type not in accepted_types:
    output_type = raw_input('Choose a file type: (html/csv/json/pdf) ')
    if output_type not in accepted_types:
        print 'Invalid input. Please enter an accepted type.'
print

# All the optional arguments for the program
print "Enter the optional arguments. Leave blank if you do not want to pass these arguments"
search_queries = raw_input('Name of file with search queries: ')
repo_list = raw_input('Name of file with list of repositories: ')
host_list = raw_input('Name of the file with the list of IP addresses ')
if not host_list:
    ip_range = raw_input('IP subnet in CIDR notation ')
duplicates = raw_input("Do you want duplicate scan results for hosts? (yes/no)") == 'yes'
email_choice = raw_input("Do you want the results to be emailed? (yes/no)") == 'yes'
columns = raw_input("What columns would you like to be filtered in? (IP, DNS, Repository, MAC, L_SEEN))")

# Make a dictionary out of the choices
js = {'user'       : user, 'pass': passwd, 'plugin_id': plugin_id,
      'search_list': search_queries, 'repo_list': repo_list,
      'host_list'  : host_list, 'ip_range': ip_range, 'duplicates': duplicates,
      'output'     : output_type, 'email_results': email_choice, 'columns': columns}

# Convert the python dictionary to a json text
js = json.dumps(js)

# Write the json text to a file
f = open(config_file, 'w')
f.write(js)
f.close()
