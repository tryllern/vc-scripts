import xmlrpclib
import optparse	


'''
Parsing of commandline options *start*

'''
p = optparse.OptionParser()
p.add_option('-i',dest="ip",metavar="<address>",help='address to vcs, ip or dns name')
p.add_option('-u',dest="username",metavar="<username>",help='Username for the vcs' )
p.add_option("-p", dest="password",metavar="<Password>",help='Password for the vcs')
p.add_option("-w",dest='warning',help='Warning level')
p.add_option("-c",dest='critical',help='Critical level')
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



'''
Functions goes here *start*
'''
def check_if_more(rawdata):
	try:
		rawdata['enumerateID']
		
		return True
	except:
		return False
		print 
def getperticipants(rawdata):
	# test['participants'][0]['conferenceName']
	audio_calls=0
	video_calls=0
	
	
	try:
		for name in rawdata['participants']:
		#print name['displayName']
	
			if name['videoRxCodec']=='none' and name['videoTxCodec']=='none':
				#print name['displayName'] + ' is a audio call'
				audio_calls=audio_calls+1
			else:
				#print name['displayName'] + ' is a video call'
				video_calls=video_calls+1
		
		return(video_calls,audio_calls)
	
	except KeyError:
		return (0,0)
'''
Functions goes here *stop*
'''



'''
Main
'''


# sets up the connection to the server
server="http://%s/RPC2"  % (options.ip) 
mcu = xmlrpclib.Server(server)
params = {
		"authenticationUser" : options.username,
		"authenticationPassword" : options.password,
		"enumerateFilter" : "connected"
		}

# Does the first call to server and gets the first 10 perticipants
mcu_data=mcu.participant.enumerate(params)

# init of counters 
video=0
audio=0

'''
If there are a ['enumerateID'] option in the answer from the server, send a new request to you don't get the ['enumerateID'] from server and count all the _active_ users
'''


if check_if_more(mcu_data)==True:
	
	(video,audio)=getperticipants(mcu_data)
	


	while check_if_more(mcu_data)==True:

	
		(video,audio)=getperticipants(mcu_data)
		params={
			"authenticationUser" : options.username,
			"authenticationPassword" : options.password,
			"enumerateFilter" : "connected",
			"enumerateID" : mcu_data['enumerateID']
		
			} 
		mcu_data=mcu.participant.enumerate(params)
		#test2=testsvr.enumerateID(params2)
		(video_tmp,audio_tmp)=getperticipants(mcu_data)
		video=video+video_tmp
		audio=audio+audio_tmp

else:
	print "False!"	
	(video,audio)=getperticipants(mcu_data)

'''
Print result and quit.....
'''	
print "video:%s audio:%s" %(video,audio)
