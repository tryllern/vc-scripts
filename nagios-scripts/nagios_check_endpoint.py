#!/usr/bin/python
import requests
import re
import optparse

p = optparse.OptionParser()
p.add_option('-i',dest="ip",metavar="<address>",help='address to codec, ip or dns name')
p.add_option('-u',dest="username",metavar="<username>",help='Username for codec' )
p.add_option("-p",dest="password",metavar="<Password>",help='Password for codec')


options, arguments = p.parse_args()


# Check if -i -u -p is commited
if options.ip is None or options.username is None or options.password is None:
    print '\n\nERROR -i -u and -p is manditory\n\n'
    p.print_help()
    exit(-1)

h323_code=0
sip_code=0
exit_text="Connection Error"


sip_response=requests.get(
    	"https://"+options.ip+'/getxml?location=/Status/SIP/Profile/Registration/Status',
    	auth=(options.username, options.password),
    	verify=False,)

if sip_response.status_code==200:
		
	regex =re.compile("<Status item=\"1\">(.+)</Status>")
	status=regex.search(sip_response.text)
	if status:
		status=status.group(1)
		if status=="Inactive":
			sip_code=1
			exit_text="SIP-Status:{}".format(status)

		elif status=="Registered":
			sip_code=0
			exit_text="SIP-Status:{}".format(status)

		elif status=="Rejected":
			sip_code=2
			exit_text="SIP-Status:{}".format(status)			

		else:
			sip_code=3
			exit_text="SIP-Status:{}".format(status)
			
			
else:
	sip_code=3

h323_response=requests.get(
    	"https://"+options.ip+'/getxml?location=/Status/H323/Gatekeeper/Status',
    	auth=(options.username, options.password),
    	verify=False,)

if h323_response.status_code==200:
	regex=re.compile("<Status item=\"1\">(.+)</Status>")
	status=regex.search(h323_response.text)
	if status:
		status=status.group(1)
		if status=="Inactive":
			h323_code=1
			exit_text +=" H323-Status:{}".format(status)

		elif status=="Registred":
			h323_code=0
			exit_text +=" H323-Status:{}".format(status)

		elif status=="Rejected":
			h323_code=2
			exit_text +=" H323-Status:{}".format(status)	

		else:
			h323_code=3
			exit_text +=" H323-Status:{}".format(status)
else:
	h323_code=3

#exit code 0
if sip_code==0 and h323_code==0:
	exit_code=0
elif sip_code==0 and h323_code==1:
	exit_code=0
elif sip_code==1 and h323_code==0:
	exit_code=0

#exit code 1
elif sip_code==1 and h323_code==1:
	exit_code=1
elif sip_code==2 and h323_code==0:
	exit_code=1
elif sip_code==0 and h323_code==2:
	exit_code=1
elif sip_code==3 and h323_code==0:
	exit_code=1
elif sip_code==0 and h323_code==3:
	exit_code=1

#exit code 2
elif sip_code==2 and h323_code==2:
	exit_code=2
elif sip_code==3 and h323_code==2:
	exit_code=2
elif sip_code==2 and h323_code==3:
	exit_code=2
	
# exit code 3
elif sip_code==3 and h323_code==3:
	exit_code=3
elif sip_code==1 and h323_code==3:
	exit_code=3
elif sip_code==3 and h323_code==1:
	exit_code=3




# print status and exit
print exit_text
exit(exit_code)
