#!/usr/bin/env python

'''
V1.2
print "Video calls:%s percent of %s in use, Audio calls:%s percent of %s in use |video_calls=%s, audio_calls=%s" %
shows percentage in use and performance data

'''
import xmlrpclib
import optparse 
import urllib2
#from urlparse import urlparse
from xml.dom.minidom import parseString
import math  # math.floor()


#Parsing of commandline options *start*
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
if options.ip is None or options.username is None or options.password is None:
    print '\n\nERROR -i -u and -p is manditory\n\n'
    p.print_help()
    exit(-1)
if options.critical is None:
    print '\n\nERROR    -c is manditory\n\n'
    p.print_help()
    exit(3)



def getMCUVideoPorts(ip,username,password):
  '''
  Retuns a tuple of total video portss and total audio ports available
  '''
  theurl='http://%s/system.xml' % ip
 
  passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
  passman.add_password(None, theurl, username, password)
  authhandler = urllib2.HTTPBasicAuthHandler(passman)
  opener = urllib2.build_opener(authhandler)
  urllib2.install_opener(opener)
  answer=urllib2.urlopen(theurl)
  answer=parseString(answer.read())
  total_video_ports=int(answer.getElementsByTagName('totalVideoPorts')[0].toprettyxml().split('\n')[1][0:])
  total_audio_ports=int(answer.getElementsByTagName('totalAudioOnlyPorts')[0].toprettyxml().split('\n')[1][0:])

  #return video_ports
  return (total_video_ports,total_audio_ports)
  


def getPerticipantsCount(ip, username, password, enumid=False, video_count=0.1, audio_count=0.1):
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
    try:
        mcu_data = mcu.participant.enumerate(params)
    except:
        print "Error connecting to the Server"
        exit(-1)

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
        # Recursive call
        return getPerticipantsCount(ip, username, password, enumid, vCount, aCount)
        
    if enumid == False:
        return(aCount,vCount)
        

# sets up the connection to the server
server="http://%s/RPC2"  % (options.ip) 
mcu = xmlrpclib.Server(server)


if not options.warning: 
    options.warning=options.critical


# Get the data from the mcu
(total_video,total_audio)=getMCUVideoPorts(options.ip,options.username,options.password)
(audio, video) = getPerticipantsCount(options.ip, options.username, options.password)      


'''
getting the floor value, the etPerticipantsCount() is called with audio/video=0.1 to avoid raising error on div by zero.
'''
audio=int(math.floor(audio))
video=int(math.floor(video))


# Do the calculations
percent_video=(float(video)/float(total_video))*100.0
percent_video=int(percent_video)
percent_audio=(float(audio)/float(total_audio))*100.0
percent_audio=int(percent_audio)

 
# print the result
if percent_video > int(options.critical):  
  print "Video Ports:%s percent of %s in use |video_calls=%s, audio_calls=%s " % (percent_video,total_video,video,audio)
  exit(2)
if percent_audio > int(options.critical):  
  print "Audio Ports:%s percent of %s in use |video_calls=%s, audio_calls=%s " % (percent_audio,total_audio,video,audio)
  exit(2)
          
if options.warning :  
        
  if percent_video  >= int(options.warning) or percent_audio  >= int(options.warning):
    print "Video calls:%s percent of %s in use, Audio calls:%s percent of %s in use |video_calls=%s, audio_calls=%s" % (percent_video,total_video,percent_audio,total_audio,video,audio)
    exit(1)
  else:
     print "Video calls:%s percent of %s in use, Audio calls:%s percent of %s in use |video_calls=%s, audio_calls=%s" % (percent_video,total_video,percent_audio,total_audio,video,audio)
     exit(0)    
        
exit(3)
