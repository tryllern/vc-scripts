import json
import requests
import xml.etree.ElementTree as ET
import re
import optparse 

p = optparse.OptionParser()
p.add_option('-i',dest="ip",metavar="<address>",help='address to acano server, ip or dns name')
p.add_option('-u',dest="username",metavar="<username>",help='Username for the acano' )
p.add_option("-p",dest="password",metavar="<Password>",help='Password for the acano')

options, arguments = p.parse_args()

if len(arguments) >= 1:
    p.error("incorrect number of arguments")

# Check if -i -u -p is commited
if options.ip is None or options.username is None or options.password is None:
    print '\n\nERROR -i -u and -p is manditory\n\n'
    p.print_help()
    exit(3)




def get_alarms(manageraddress,username,password):
	response=requests.get("https://"+manageraddress+"/api/v1/system/alarms",
						auth=(username,password),
						verify=False,
						)
	if response.status_code==200:
				return response

	else:
				return "Error"		

response=get_alarms(options.ip,options.username,options.password)
if response=="Error":
	print "could not connect to server!"
	exit(3)
alarms= re.search(r'<?xml version="1.0"?><alarms>(.+)</alarms>',response.text,re.M|re.I)
try:
	a=alarms.group(1)
	print "Alarm:{}".format(a)
	exit(2)
except:
	print "Alarms:0"
	exit(0)




