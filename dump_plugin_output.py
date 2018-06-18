#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
dump_plugin_output.py

This module works with Tenable Security Center's RESTful APIs to retrieve information about system scans. User is asked
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
IP_LENGTH = 4


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
def get_repo_ids(requested_repo_names, all_repo_data):
    repo_ids = []

    for requested_repo_name in requested_repo_names:
        for repository in all_repo_data['response']:
            if requested_repo_name == repository['name']:
                repo_ids.append(repository['id'])
                break

    return ",".join(repo_ids)


# 		dump_plugin_data()
#
# Function that defines the flow in dumpPlugin.py. It opens a connection to Security Center, retrieves the information
# about the desired plugin, and dumps it all to a .dump file.
# Input  - plugin_id, a string of the plugin_id whose output is to be dumped
# Output - none, write to file
def dump_plugin_data(plugin_id, requested_repo_names, host_list, ip_range):
    # Establish connection, retrieve data
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

    case_num = 1
    obj = []
    temp_obj = {'ID': '', 'IP': '', 'DNS': '', 'REPO': '', 'CONTENT': []}
    
    for case in output:
        temp_obj['ID'] = case_num
        temp_obj['IP'] = case[u'ip']
        temp_obj['MAC'] = case[u'macAddress']
        temp_obj['DNS'] = case[u'dnsName']
        temp_obj['REPO'] = case[u'repository'][u'name']
        temp_obj['L_SEEN'] = case[u'lastSeen']
        temp_obj['CONTENT'] = case[u'pluginText'].split('\n')

        obj.append(temp_obj.copy())
        case_num += 1

    # Convert to JSON, write to file
    ob = json.dumps(obj)
    f = open(OUTPUT_FILE, 'w')
    f.write(ob)
