#!/usr/bin/env python
#coding: utf8
#Version 1.1

import xmlrpclib
import optparse

'''
Parsing of commandline options *start*

'''
p = optparse.OptionParser()
p.add_option('-i', dest="ip", metavar="<address>", help='address to vcs')
p.add_option('-u', dest="username", metavar="<username>", help='Username')
p.add_option("-p", dest="password", metavar="<Password>", help='Password')
p.add_option("-w", dest='warning', help='Warning level')
p.add_option("-c", dest='critical', help='Critical level')
options, arguments = p.parse_args()

if len(arguments) >= 1:
	p.error("incorrect number of arguments")

# Check if -i -u -p is commited
if options.ip is None:
	print '\n\nERROR -i is manditory\n\n'
	p.print_help()
	exit(-1)
if options.username is None:
	print '\n\nERROR -u is manditory\n\n'
	p.print_help()
	exit(-1)
if options.password is None:
	print '\n\nERROR -p is manditory\n\n'
	p.print_help()
	exit(-1)
if options.critical is None:
	print '\n\nERROR    -c is manditory\n\n'
	p.print_help()
	exit(3)


'''
Parsing of commandline options *stop*

'''

# sets up the connection to the server
server = "http://%s/RPC2" % options.ip
isdn_server = xmlrpclib.Server(server)


def get_active_calls(server, username, password, port):
	params = {
			"authenticationUser" : username,
			"authenticationPassword" : password,
			"port" : port 
			}
				
	isdn_data = server.isdn.port.query(params)
	
	if isdn_data['enabled']==0:  # if the isdn port is not active, return 0
		return(0,0)

	if isdn_data['enabled']==1:  # if the isdn port is active report ports in use
		c=0
		f=0
		for channels in isdn_data['bChannels']:
	 
			if (channels['active']==True):
				c=c+1
	
			if (channels['active']==False):
				f=f+1
	return (c,f)



ports_in_use=0  # init of the active ports counter
ports_not_in_use=0

for i in range(4):   # there are up to four physical isdn ports, go trough all of them and count active lines
	
	(tmp_c,tmp_f)=get_active_calls(isdn_server,options.username,options.password,i)
	ports_in_use=ports_in_use+tmp_c
	ports_not_in_use=ports_not_in_use+tmp_f

isdn_Available_Channels=ports_in_use+ports_not_in_use
if int(ports_in_use)==0:
	ports_in_use=0.1
if int(isdn_Available_Channels)==0:
	isdn_Available_Channels=0.1	

percent_active_ports=int((float(ports_in_use)/float(isdn_Available_Channels))*100.0)

if ports_in_use==0.1:
	ports_in_use=0
if isdn_Available_Channels==0.1:
	isdn_Available_Channels=0
	
if percent_active_ports > int(options.critical):  
  print "%i ISDN Channels(%s percent) of %s in use | Current=%s" % (ports_in_use,percent_active_ports,isdn_Available_Channels,ports_in_use)
  exit(2)

if options.warning:  
  if percent_active_ports  > int(options.warning):
    print "%i ISDN Channels(%s percent) of %s in use |Current=%s" % (ports_in_use,percent_active_ports,isdn_Available_Channels,ports_in_use)
    exit(1)
  else:
     print "%i ISDN Channels(%s percent) of %s in use |Current=%s" % (ports_in_use,percent_active_ports,isdn_Available_Channels,ports_in_use)
     exit(0)	
    	
exit(3)
