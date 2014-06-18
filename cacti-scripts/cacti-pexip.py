#UTF8
import json
import requests
import optparse 

p = optparse.OptionParser()
p.add_option('-i',dest="ip",metavar="<address>",help='address to Pexip manager server, ip or dns name')
p.add_option('-u',dest="username",metavar="<username>",help='Username for Pexip manager server' )
p.add_option("-p",dest="password",metavar="<Password>",help='Password for Pexip manager server')
options, arguments = p.parse_args()

if len(arguments) >= 1:
    p.error("incorrect number of arguments")

# Check if -i -u -p is commited
if options.ip is None or options.username is None or options.password is None:
    print '\n\nERROR -i -u and -p is manditory\n\n'
    p.print_help()
    exit(-1)





def how_many_in_conference(mgr,username,password,conference_name):
	response=requests.get(
    	"https://"+mgr+'/api/admin/status/v1/participant/?conference='+conference_name,
    	auth=(username, password),
    	verify=False,)
	return json.loads(response.text)['meta']['total_count']	


active_conferences=requests.get("https://"+options.ip+"/api/admin/status/v1/conference/",auth=(options.username,options.password),verify=False)

counter=0
for conf in json.loads(active_conferences.text)['objects']:
    counter +=int(how_many_in_conference(options.ip,options.username,options.password,conf['name']))

print "perticipants:%d" %counter

