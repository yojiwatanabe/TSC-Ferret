from securitycenter import SecurityCenter5
import json
import getpass

HOST = 'sec-center-prod-01.uit.tufts.edu'

user = input("Username: ")
pw = getpass.getpass()
sc = SecurityCenter5(HOST)
sc.login(user, pw)


output = sc.analysis(('pluginID', '=', '22869'), tool='vulndetails')
case_num = 1
total_cases = len(output)
obj = []
temp_obj = {'IP':'', 'DNS':'', 'REPO':'', 'CONTENT':''}
for case in output:
	# print '##### CASE ' + str(case_num) + "/" + str(total_cases)
	temp_obj['IP'] = case[u'ip']
	# print 'IP Address: ' + case[u'ip']
	temp_obj['DNS'] = case[u'dnsName']
	# print 'DNS: ' + case[u'dnsName']
	temp_obj['REPO'] = case[u'repository'][u'name']
	temp_obj['CONTENT'] = case[u'pluginText']
	# print 'Repository: ' + case[u'repository'][u'name']
	# print case[u'pluginText']
	obj.append(json.dumps(temp_obj))
	temp_obj.clear()
ob = json.dumps(obj)

f = open('pluginText.dump', 'w')
f.write(ob)