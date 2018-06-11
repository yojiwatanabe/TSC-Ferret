#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
dumpPluginOut.py

This module works with Tenable Security Center's RESTful APIs to retrieve information about system scans. User is asked
to authenticate their session, after which they are able to get the plugin output from scans performed on hosts. This
module simply retrieves the data and saves it into 'pluginText.dump', after which it is processed by the 'processDump'
module and made human-friendly.ß
'''

import json
import getpass
from securitycenter import SecurityCenter5

HOST         = 'sec-center-prod-01.uit.tufts.edu'
OUTPUT_FILE  = 'pluginText.dump'


# 		loginSC()
#
# Function to open a connection with the specified Security Center 5 host. Asks user for their login information and
# then proceeds to try to establish an authenticated connection.
# Input  - none
# Output - Authenticated SecurityCenter5 object
def loginSC():
    user = raw_input("Username: ")
    pw   = getpass.getpass()
    sc   = SecurityCenter5(HOST)

    sc.login(user, pw)
    return sc


# 		dumpDataRepoQuery()
#
# Function to save all queried information for hosts in a specified repository/repositories
# Input  - repolist: string list with repositories to include in output
#          output: dictionary list with the plugin output from all hosts/repos with host information
# Output - dictionary list with the plugin output of hosts in the specified repository
def dumpDataRepoQuery(repoList, output):
    case_num = 1
    obj = []
    temp_obj = {'ID': '', 'IP': '', 'DNS': '', 'REPO': '', 'CONTENT': []}
    for case in output:
        if case[u'repository'][u'name'] not in repoList:
            continue
        temp_obj['ID']      = case_num
        temp_obj['IP']      = case[u'ip']
        temp_obj['MAC'] = case[u'macAddress']
        temp_obj['DNS']     = case[u'dnsName']
        temp_obj['REPO']    = case[u'repository'][u'name']
        temp_obj['L_SEEN']  = case[u'lastSeen']
        temp_obj['CONTENT'] = case[u'pluginText'].split("\n")

        obj.append(temp_obj.copy())
        case_num += 1

    return obj


# 		dumpDataHostQuery()
#
# Function to save all queried information for the specified host/hosts
# Input  - hostlist: string list with IP addresses of hosts to include in output
#          output: dictionary list with the plugin output from all hosts/repos with host information
# Output - dictionary list with the plugin output of hosts within the defined IP address range
def dumpDataHostQuery(hostList, output):
    case_num = 1
    obj = []
    temp_obj = {'ID': '', 'IP': '', 'DNS': '', 'REPO': '', 'CONTENT': []}
    for case in output:
        if case[u'ip'] not in hostList:
            continue
        temp_obj['ID']      = case_num
        temp_obj['IP']      = case[u'ip']
        temp_obj['MAC']     = case[u'macAddress']
        temp_obj['DNS']     = case[u'dnsName']
        temp_obj['REPO']    = case[u'repository'][u'name']
        temp_obj['L_SEEN']  = case[u'lastSeen']
        temp_obj['CONTENT'] = case[u'pluginText'].split("\n")

        obj.append(temp_obj.copy())
        case_num += 1

    return obj


# 		dumpDataIPrange()
#
# Function to save all queried information that falls within the range of IPs
# Input  - ipMin: lower IP address boundary
#          ipMax: upper IP address boundary
#          output: dictionary list with the plugin output from all hosts/repos with host information
# Output - dictionary list with the plugin output of hosts within the defined IP address range
def dumpDataIPrange(ipMin, ipMax, output):
    case_num = 1
    obj = []
    temp_obj = {'ID': '', 'IP': '', 'DNS': '', 'REPO': '', 'CONTENT': []}
    for case in output:
        if case[u'ip'] < ipMin or case[u'ip'] > ipMax:
            continue
        temp_obj['ID']      = case_num
        temp_obj['IP']      = case[u'ip']
        temp_obj['MAC'] = case[u'macAddress']
        temp_obj['DNS']     = case[u'dnsName']
        temp_obj['REPO']    = case[u'repository'][u'name']
        temp_obj['L_SEEN']  = case[u'lastSeen']
        temp_obj['CONTENT'] = case[u'pluginText'].split("\n")

        obj.append(temp_obj.copy())
        case_num += 1

    return obj


# 		dumpPluginData()
#
# Function that defines the flow in dumpPlugin.py. It opens a connection to Security Center, retrieves the information
# about the desired plugin, and dumps it all to a .dump file.
# Input  - pluginID, a string of the pluginID whose output is to be dumped
# Output - none, write to file
def dumpPluginData(pluginID, repoList, hostList, ipRange):
    # Establish connection, retrieve data
    sc = loginSC()
    output = sc.analysis(('pluginID', '=', pluginID), tool='vulndetails')

    if repoList:
        f = open(repoList, 'r')
        obj = dumpDataRepoQuery(f.read(), output)
    elif hostList:
        f = open(hostList, 'r')
        obj = dumpDataHostQuery(f.read(), output)
    elif ipRange:
        [ipMin, ipMax] = ipRange.split('-')
        obj = dumpDataIPrange(ipMin, ipMax, output)
    else:
        # Build JSON structure with data retrieved
        case_num = 1
        obj = []
        temp_obj = {'ID': '', 'IP': '', 'DNS': '', 'REPO': '', 'CONTENT': []}
        for case in output:
            temp_obj['ID']      = case_num
            temp_obj['IP']      = case[u'ip']
            temp_obj['MAC']     = case[u'macAddress']
            temp_obj['DNS']     = case[u'dnsName']
            temp_obj['REPO']    = case[u'repository'][u'name']
            temp_obj['L_SEEN']  = case[u'lastSeen']
            temp_obj['CONTENT'] = case[u'pluginText'].split("\n")

            obj.append(temp_obj.copy())
            case_num += 1

    # Convert to JSON, write to file
    ob = json.dumps(obj)
    f = open(OUTPUT_FILE, 'w')
    f.write(ob)