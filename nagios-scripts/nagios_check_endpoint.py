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



def getline(ip,username,password,url,identifier):

	'''
	ip= address to codec
	username= username to codec
	passord= passowrd to codec
	url= the part after getxml?location=' to extract from codec
	identifier= the regex search-string
	'''
	response=requests.get(
    	"https://"+ip+'/getxml?location='+url,
    	auth=(username, password),
    	verify=False,)
	if response.status_code==200:
		regex=re.compile(identifier)
		status=regex.search(response.text)
		if status:
			return status.group(1)
		else:
			return None
	else:
		return None




software_version=getline(ip=options.ip,
					  username=options.username,
					  password=options.password,
					  url="/Status/SystemUnit/Software/Version",
					  identifier='<Version item=\"1\">(.+)</Version>'
					  )

if software_version:
	if software_version.lower().startswith("tc"):
		

			sip_response=getline(ip=options.ip,
								  username=options.username,
								  password=options.password,
								  url="/Status/SIP/Profile/Registration/Status",
								  identifier='<Status item=\"1\">(.+)</Status>'
								  )


			if sip_response:		
				
				
					status=sip_response.lower()
					if status=="inactive":
						sip_code=1
						exit_text="SIP-Status:{}".format(status)

					elif status=="registered":
						sip_code=0
						exit_text="SIP-Status:{}".format(status)

					elif status=="rejected":
						sip_code=2
						exit_text="SIP-Status:{}".format(status)			

					else:
						sip_code=3
						exit_text="SIP-Status:{}".format(status)
						
						
			else:
				sip_code=3



			h323_response=getline(ip=options.ip,
								  username=options.username,
								  password=options.password,
								  url="/Status/H323/Gatekeeper/Status",
								  identifier='<Status item=\"1\">(.+)</Status>'
								  )

			if h323_response:

				
					status=h323_response.lower()
					if status=="inactive":
						h323_code=1
						exit_text +=" H323-Status:{}".format(status)

					elif status=="registered":
						h323_code=0
						exit_text +=" H323-Status:{}".format(status)

					elif status=="rejected":
						h323_code=2
						exit_text +=" H323-Status:{}".format(status)	

					else:
						h323_code=3
						exit_text +=" H323-Status:{}".format(status)
			else:
				
				h323_code=3


	if software_version.lower().startswith("f"):

			sip_response=getline(ip=options.ip,
					  username=options.username,
					  password=options.password,
					  url="/Status/SIP/Registration",
					  identifier='<Registration item="1" status="(.+)">'
					  )


			if sip_response:		
				
				
					status=sip_response.lower()
					if status=="inactive":
						sip_code=1
						exit_text="SIP-Status:{}".format(status)

					elif status=="registered":
						sip_code=0
						exit_text="SIP-Status:{}".format(status)

					elif status=="rejected":
						sip_code=2
						exit_text="SIP-Status:{}".format(status)			

					else:
						sip_code=3
						exit_text="SIP-Status:{}".format(status)
						
						
			else:
				sip_code=3



			h323_response=getline(ip=options.ip,
					  username=options.username,
					  password=options.password,
					  url="/Status/H323GateKeeper",
					  identifier='<H323Gatekeeper item="1" status="(.+)">'
					  )

			if h323_response:

				
					status=h323_response.lower()
					if status=="inactive":
						h323_code=1
						exit_text +=" H323-Status:{}".format(status)

					elif status=="registered":
						h323_code=0
						exit_text +=" H323-Status:{}".format(status)

					elif status=="rejected":
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
