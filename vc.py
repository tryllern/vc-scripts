#!/usr/bin/env python
#coding: utf8 


import sys
import ConfigParser
import os
import optparse	
import urllib2


'''
checking options
'''
p = optparse.OptionParser()
p.add_option('--call','-c',dest="call",metavar="<number>")
p.add_option("-d", "--disconnect", dest="disconnect",action="store_const", const=1)
p.add_option("-m","--mute",dest="mute", action="store_const", const=1)
p.add_option("-u","--unmute",dest="unmute",action="store_const", const=1)

options, arguments = p.parse_args()
if len(arguments) >= 1:
  p.error("incorrect number of arguments")
'''
End of options check
'''



'''
Config file loading and checking
'''
Config = ConfigParser.ConfigParser()
homedir= os.getenv("HOME")
configfile='%s/.tandberg' % homedir
if not os.path.exists(configfile):

  print "Can't find config file, genrerating file...\n"
  new_config = ConfigParser.RawConfigParser()
  new_config.add_section("system")
  input_ip= raw_input("Address(ip) to Unit: ")
  new_config.set("system","ip",'%s' % input_ip)
  input_username=raw_input("Username: ")
  new_config.set("system","username",'%s' % input_username)
  input_username=raw_input("Password: ")
  new_config.set("system","password",'%s' % input_username)
  with open(configfile, 'wb') as nyfil:
    new_config.write(nyfil) 
    print "saving config in ~/.tandberg"

try:
  Config.read(configfile)
except Exception:
  print "Error reading config file, quitting...1"
  quit()
try:
  ip=Config.get('system','ip')
  username=Config.get('system','username')
  password=Config.get('system','password')
except Exception:
  print "Error reading config file, quitting...2"
  quit()




def getxml(ip,username,password,request):
  
  theurl='http://%s/getxml?location=' % ip
 
  passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
  passman.add_password(None, theurl, username, password)
  authhandler = urllib2.HTTPBasicAuthHandler(passman)
  opener = urllib2.build_opener(authhandler)
  urllib2.install_opener(opener)
  answer= urllib2.urlopen(theurl + urllib2.quote(request))
  return answer.read()
def putDial(ip,username,password,number):
  '''
  Description:
			Dials a number
  Parameters:
			ip - 		the ip adress of the codec
			username -	username, usally 'admin'
			password - 	password, on te/tc plattform the default is <blank> on MXP its 'TANDBERG'
			number - 	Number to dial 
			
  Dependencies:
			putxml()
  '''
  
  
  
  
  request='<Command><Dial command="True"><Number>%s</Number></Dial></Command>' % (number)
  return putxml(ip,username,password,request)
def putxml(ip,username,password,request):
  
  theurl='http://%s/formputxml?xmldoc=' % ip
 
  passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
  passman.add_password(None, theurl, username, password)
  authhandler = urllib2.HTTPBasicAuthHandler(passman)
  opener = urllib2.build_opener(authhandler)
  urllib2.install_opener(opener)
  answer= urllib2.urlopen(theurl + urllib2.quote(request))
  return answer.read()
def putDisconnectAll(ip,username,password):
  ''' 
    Description:
			Disconnects all active calls
  
    Parameters:
			ip - 		the ip adress of the codec
			username -	username, usally 'admin'
			password - 	password, on te/tc plattform the default is <blank> on MXP its 'TANDBERG'
  
    Dependencies:
			putxml()
  
  '''
  request='<Command><Call><DisconnectAll command="True"></DisconnectAll></Call></Command>'
  return putxml(ip,username,password,request)
def putMute(ip,username,password):
  '''
   Mutes the microphone 
   
   Parameters:
			ip - 		the ip adress of the codec
			username -	username, usally 'admin'
			password - 	password, on te/tc plattform the default is <blank> on MXP its 'TANDBERG'
  
  '''
  request='<Command><Audio><Microphones><Mute command="True"></Mute></Microphones></Audio></Command>'
  return putxml(ip,username,password,request)
def putUnmute(ip,username,password):
  '''
  Unmutes the microphone
  
  Parameters:
			ip - 		the ip adress of the codec
			username -	username, usally 'admin'
			password - 	password, on te/tc plattform the default is <blank> on MXP its 'TANDBERG'
  
  '''
  request='<Command><Audio><Microphones><Unmute command="True"></Unmute></Microphones></Audio></Command>'
  return putxml(ip,username,password,request)


if options.mute:
  putMute(ip,username,password)
if options.call:
 putDial(ip,username,password,options.call)  
if options.disconnect:
 putDisconnectAll(ip,username,password)
if options.unmute:
  putUnmute(ip,username,password)
  
 





