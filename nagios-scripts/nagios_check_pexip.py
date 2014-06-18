#!/usr/bin/env python
#coding: utf8 
import json
import requests
import optparse 


'''
Daniel Nilsen - daniel@narver.net

Nagios script for pexip mcu

exit codes

0 - Ok
1 - warning
2 - critical
3 - unknown

Warning 
Critical - manditory

'''


def how_many_in_conference(mgr,username,password,conference_name):
	response=requests.get(
    	"https://"+mgr+'/api/admin/status/v1/participant/?conference='+conference_name,
    	auth=(username, password),
    	verify=False,)
	return json.loads(response.text)['meta']['total_count']	


p = optparse.OptionParser()
p.add_option('-i',dest="ip",metavar="<address>",help='address to Pexip manager server, ip or dns name')
p.add_option('-u',dest="username",metavar="<username>",help='Username for Pexip manager server' )
p.add_option("-p",dest="password",metavar="<Password>",help='Password for Pexip manager server')
p.add_option("-w",dest='warning',help='Warning level')
p.add_option("-c",dest='critical',help='Critical level')

options, arguments = p.parse_args()

if len(arguments) >= 1:
    p.error("incorrect number of arguments")

# Check if -i -u -p is commited
if options.ip is None or options.username is None or options.password is None:
    print '\n\nERROR -i -u and -p is manditory\n\n'
    p.print_help()
    exit(-1)

if options.critical is None:
	print '\n\nERROR    -c is manditory\n\n'
	p.print_help()
	exit(3)

# if the warning options is not defined, set it as the same as critical
if not options.warning: options.warning=options.critical


# Get active conferences
active_conferences=requests.get("https://"+options.ip+"/api/admin/status/v1/conference/",auth=(options.username,options.password),verify=False)

# loop through all the conferences and count the perticipants
counter=0
for conf in json.loads(active_conferences.text)['objects']:
    print conf
    counter +=int(how_many_in_conference(options.ip,options.username,options.password,conf['name']))


output_text="active_ports:%d " % counter

# if it is no active perticipants, everything is definitely ok
if counter==0:
	
	exit(0)


if counter >= int(options.critical):
	print output_text
	exit(2)
elif counter >=int(options.warning):
	print output_text
	exit(1)
elif counter < int(options.warning):
	print output_text
	exit(0)
else:
	print output_text
	exit(3)