# -*- coding: utf-8 -*-

from securitycenter import SecurityCenter5
import json
import getpass

HOST = 'sec-center-prod-01.uit.tufts.edu'


# 		loginSC()
#
# Function to open a connection with the specified Security Center 5 host. Asks
# user for their login information and then proceeds to try to establish an 
# authenticated connection.
# Input  - none
# Output - SecurityCenter5 object of an authenticated connection
def loginSC():
    user = raw_input("Username: ")
    pw   = getpass.getpass()
    sc   = SecurityCenter5(HOST)

    sc.login(user, pw)
    return sc


# Establish connection, retrieve data
sc = loginSC()
output = sc.analysis(('pluginID', '=', '22869'), tool='vulndetails')

# Build JSON structure with data retrieved
case_num = 1
obj = []
temp_obj = {'ID': '', 'IP': '', 'DNS': '', 'REPO': '', 'CONTENT': []}
for case in output:
    program_list        = case[u'pluginText'].split("\n")
    temp_obj['ID']      = case_num
    temp_obj['IP']      = case[u'ip']
    temp_obj['DNS']     = case[u'dnsName']
    temp_obj['REPO']    = case[u'repository'][u'name']
    temp_obj['CONTENT'] = program_list[3:-1]
    obj.append(temp_obj.copy())
    case_num += 1

# Convert to JSON, write to file
ob = json.dumps(obj)
f = open('pluginText.dump', 'w')
f.write(ob)
