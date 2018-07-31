#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
dump_plugin_output.py

This module works with Tenable Security Center's APIs to retrieve information about system scans. User is asked
to authenticate their session, after which they are able to get the plugin output from scans performed on hosts. This
module simply retrieves the data and saves it into 'pluginText.dump', after which it is processed by the 'processDump'
module and made human-friendly.
"""


import json
import getpass
import process_dump
from securitycenter import SecurityCenter5

HOST = 'sec-center-prod-01.uit.tufts.edu'
OUTPUT_FILE = 'pluginText.dump'


# 		login_sc()
#
# Function to open a connection with the specified Security Center 5 host. Asks user for their login information and
# then proceeds to try to establish an authenticated connection.
# Input  - none
# Output - authenticated SecurityCenter5 object
def login_sc():
    user = raw_input("Username: ")
    pw = getpass.getpass()
    sc = SecurityCenter5(HOST)

    sc.login(user, pw)
    return sc


#       get_repo_ids()
#
# Takes in the requested repository names and all repository data and returns the requested repositories' IDs, which is
# used by dump_plugin_data() to request scan information about specific repositories
# Input  - requested_repo_names: list of strings of the repositories to query for\
#          all_repo_data: dictionary object with all data pertaining to scanned repositories
# Output - String with repository IDs separated by commas
def get_repo_ids(requested_repo_names, all_repo_data):
    repo_ids = []

    for requested_repo_name in requested_repo_names:
        for repository in all_repo_data['response']:
            if requested_repo_name == repository['name']:
                repo_ids.append(repository['id'])
                break

    if len(repo_ids) < 1:
        print 'Could not find repository. Exiting program...'
        exit(1)

    return ",".join(repo_ids)


#       is_not_latest_scan()
#
# Checks whether the current scan details are part of the latest scan against a given host
# Input  - ip_address: unicode string of current IP address
#          scan_date: unicode string of the date the scan took place (note: in SecurityCenter is the same as last seen)
#          stored_scans: dictionary list of the already gathered scan data
# Output - Boolean value indicating whether or not this information is the most current available
def is_not_latest_scan(ip_address, scan_date, stored_scans):
    for scan_info in stored_scans:
        if (ip_address == scan_info['IP']) & (int(scan_date) < int(scan_info['L_SEEN'])):
            return True

    return False


# 		dump_plugin_data()
#
# Function that defines the flow in dumpPlugin.py. It opens a connection to Security Center, retrieves the information
# about the desired plugin, and dumps it all to a .dump file.
# Input  - plugin_id: a string of the plugin_id whose output is to be dumped
# Output - none, write to file

def dump_plugin_data(plugin_id, requested_repo_names, host_list, ip_range, allow_duplicates, user, pw):
    # Establish connection, retrieve data
    if user and pw:
        sc = SecurityCenter5(HOST)
        sc.login(user, pw)
    else:
        sc = login_sc()
        
    arg_tuples = [('pluginID', '=', plugin_id)]

    if requested_repo_names:
        requested_repo_names = process_dump.read_input(requested_repo_names)
        all_repo_data = sc.get('/repository')
        requested_repo_ids = get_repo_ids(requested_repo_names, all_repo_data.json())
        arg_tuples.append(('repositoryIDs', '=', requested_repo_ids))

    if host_list:
        hosts = process_dump.read_input(host_list)
        arg_tuples.append(('ip', '=', ",".join(hosts)))
    elif ip_range:
        arg_tuples.append(('ip', '=', ip_range))

    output = sc.analysis(*arg_tuples, tool='vulndetails')
    if not output:
        print 'No results found. Exiting program'
        exit(0)

    obj = []
    temp_obj = {'ID': '', 'IP': '', 'DNS': '', 'REPO': '', 'CONTENT': []}

    for case in output:
        if is_not_latest_scan(case[u'ip'], case[u'lastSeen'], obj) & (allow_duplicates is False):
            continue

        temp_obj['ID'] = obj.__len__()
        temp_obj['IP'] = case[u'ip']
        temp_obj['MAC'] = case[u'macAddress']
        temp_obj['DNS'] = case[u'dnsName']
        temp_obj['REPO'] = case[u'repository'][u'name']
        temp_obj['L_SEEN'] = case[u'lastSeen']
        temp_obj['CONTENT'] = case[u'pluginText'].split('\n')

        obj.append(temp_obj.copy())

    # Convert to JSON, open and write to file
    ob = json.dumps(obj)
    f = open(OUTPUT_FILE, 'w')
    f.write(ob)
