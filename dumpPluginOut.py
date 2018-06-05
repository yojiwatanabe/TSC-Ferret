from securitycenter import SecurityCenter5
from base64 import b64decode
import json
import getpass

HOST = 'sec-center-prod-01.uit.tufts.edu'

user = raw_input("Username: ")
pw = getpass.getpass()
sc = SecurityCenter5(HOST)
sc.login(user, pw)


output = sc.analysis(('pluginID', '=', '22869'), tool='vulndetails')
case_num = 1
total_cases = len(output)
for case in output:
	print '##### CASE ' + str(case_num) + "/" + str(total_cases)
	print 'IP Address: ' + case[u'ip']
	print 'DNS: ' + case[u'dnsName']
	print 'Repository: ' + case[u'repository'][u'name']
	print case[u'pluginText']
	print

	case_num += 1
