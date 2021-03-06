#!/usr/bin/env python
# Version 1.1

import xmlrpclib
import optparse	
import urllib2
from urlparse import urlparse
from xml.dom.minidom import parseString


p = optparse.OptionParser()
p.add_option('-i',dest="ip",metavar="<address>",help='address to vcs, ip or dns name')
p.add_option('-u',dest="username",metavar="<username>",help='Username for the vcs' )
p.add_option("-p", dest="password",metavar="<Password>",help='Password for the vcs')

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






def getMCUVideoPorts(ip,username,password):
  '''
  Retuns a tuple of total video ports and total audio ports available
  '''
  theurl='http://%s/system.xml' % ip
 
  passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
  passman.add_password(None, theurl, username, password)
  authhandler = urllib2.HTTPBasicAuthHandler(passman)
  opener = urllib2.build_opener(authhandler)
  urllib2.install_opener(opener)
  answer=urllib2.urlopen(theurl)
  answer=parseString(answer.read())
  
  total_video_ports=answer.getElementsByTagName('totalVideoPorts')[0].toprettyxml().split('\n')[1][0:]
  total_audio_ports=answer.getElementsByTagName('totalAudioOnlyPorts')[0].toprettyxml().split('\n')[1][0:]

  #return video_ports
  return (total_video_ports,total_audio_ports)
  

# sets up the connection to the server
server="http://%s/RPC2"  % (options.ip) 
mcu = xmlrpclib.Server(server)
def getPerticipantsCount(ip, username, password, enumid=False, video_count=0, audio_count=0):
	vCount=0
	aCount=0

	if enumid == False :	
			params = {
					"authenticationUser" : username,
					"authenticationPassword" : password,
					"enumerateFilter" : "connected"
					}
			
					
	if enumid != False:  # if there is more than 10 calls
		params = {
			"authenticationUser": username,
			"authenticationPassword": password,
			"enumerateFilter": "connected",
			"enumerateID": enumid
				} 
		enumid=False
		

	# Extracting the data from the answer	
	mcu_data = mcu.participant.enumerate(params)


	try:
		enumid = mcu_data["enumerateID"]
	except:
		enumid = False
	
	try:
		for name in mcu_data['participants']:
	
			if name['videoRxCodec'] == 'none' and name['videoTxCodec'] == 'none':
				aCount = aCount + 1
			else:
				vCount = vCount + 1

	except KeyError:
		vCount = 0
		aCount = 0
	

	vCount=vCount+video_count
	aCount=aCount+audio_count

	
	if enumid != False:
		
		return getPerticipantsCount(ip, username, password, enumid, vCount, aCount)
		
	if enumid == False:
		return(aCount,vCount)
		


(total_video,total_audio)=getMCUVideoPorts(options.ip,options.username,options.password)
(audio, video) = getPerticipantsCount(options.ip, options.username, options.password)      
      

print "Video_use:%s  Video_max:%s Audio_use:%s  Audio_max:%s " % (video,total_video,audio,total_audio)
  
      
