#!/usr/bin/env python
#coding: utf8
import json
import requests
import xml.etree.ElementTree as ET
import re
import optparse 

p = optparse.OptionParser()
p.add_option('-i',dest="ip",metavar="<address>",help='address to acano server, ip or dns name')
p.add_option('-u',dest="username",metavar="<username>",help='Username for the acano' )
p.add_option("-p",dest="password",metavar="<Password>",help='Password for the acano')
p.add_option("-c",dest="critical",metavar="<Critical>",help="Critical level of ports")
p.add_option("-w",dest="warning",metavar="<Warning>",help="Warning level of ports")
p.add_option("-m",dest="max",metavar="<Max>",help="Max calls the server can handle")
options, arguments = p.parse_args()

if len(arguments) >= 1:
    p.error("incorrect number of arguments")


if options.ip is None or options.username is None or options.password is None:
    print '\n\nERROR -i -u and -p is manditory\n\n'
    p.print_help()
    exit(3)


if options.critical is None:
	print '\n\nERROR    -c is manditory\n\n'
	p.print_help()
	exit(3)


def get_status(manageraddress,user,password):

		response=requests.get("https://"+manageraddress+"/api/v1/system/status",
						auth=(user,password),
						verify=False,
						)
		
		return response
	

response=get_status(options.ip,options.username,options.password)

if response.status_code!=200:
	print "could not connect to server, error code:{}".format(response.status_code)
	exit(3)
else:
	active_ports= int(re.search(r'.*<callLegsActive>(.*)</callLegsActive>.*',response.text,re.M|re.I).group(1))

	if not options.warning:
		warning=int(options.critical)

	critical=int(options.critical)

	if not options.max:
		max_calls=options.critical
	else:
		max_calls=options.max

	if active_ports==0:
		exit_code=0
	if active_ports <=warning:
		exit_code=0
	if active_ports >=warning:
		exit_code=1
	if active_ports >=critical:
		exit_code=2


	if active_ports==0:
		print "utilization:0% |active_ports:0:{}:{}".format(warning,critical)
	else:
		percent_active_ports=int((float(active_ports)/float(max_calls))*100.0)
		print "utilization:{}% |active_ports:{};{};{}".format(percent_active_ports,active_ports,warning,critical)

	exit(exit_code)
