#!/usr/bin/env python
#coding: utf8 
'''
Format of .tandberg file

[system]
ip=192.168.1.139
username=admin
password=TANDBERG


'''

import sys
import ConfigParser
import os
import optparse	
import urllib2
import re



class codec:
	
	def __init__(self):
		
		self._readConfig()
		self.lastCommand="__init__"
		self.status="OK"
	def _readConfig(self):
		
		'''
		Config file loading and checking
		'''
		Config = ConfigParser.ConfigParser()
		homedir= os.getenv("HOME")
		configfile='%s/.tandberg' % homedir
		if not os.path.exists(configfile):
			raise NameError('Could not find config file')

		try:
			Config.read(configfile)
		except Exception:
			raise NameError("Error reading config file, quitting...")
  
		try:
			self.ip=Config.get('system','ip')
			self.username=Config.get('system','username')
			self.password=Config.get('system','password')
			#self.systemtype=Config.get('system','password')
		except Exception:
			raise( "Error reading config file, quitting...")
  

		
	def _getxml(self,request):
  
		theurl='http://%s/getxml?location=' % self.ip
 
		passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
		passman.add_password(None, theurl, self.username, self.password)
		authhandler = urllib2.HTTPBasicAuthHandler(passman)
		opener = urllib2.build_opener(authhandler)
		urllib2.install_opener(opener)
		answer= urllib2.urlopen(theurl + urllib2.quote(request))
		return answer.read()		

	
	def _putxml(self,request):
  
		theurl='http://%s/formputxml?xmldoc=' % self.ip
 
		passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
		passman.add_password(None, theurl, self.username, self.password)
		authhandler = urllib2.HTTPBasicAuthHandler(passman)
		opener = urllib2.build_opener(authhandler)
		urllib2.install_opener(opener)
		answer= urllib2.urlopen(theurl + urllib2.quote(request))
		return answer.read()
	
	
	
	def Dial(self,number):

		regex=re.compile('<Command>.*status="(.+)".*') 
		request='<Command><Dial command="True"><Number>%s</Number></Dial></Command>' % (number)
		answer=regex.search(self._putxml(request))
		self.status=answer.group(1)
		self.lastCommand="Dial"
		return self.status
	
	def DisconnectAll(self):
		
		regex=re.compile('<Command>.*status="(.+)".*')
		request='<Command><Call><DisconnectAll command="True"></DisconnectAll></Call></Command>'
		answer=regex.search(self._putxml(request))
		self.status=answer.group(1)
		self.lastCommand="DisconnectAll"
		return self.status
	
	def Mute(self):
		
		regex=re.compile('<Command>.*status="(.+)".*')
		request='<Command><Audio><Microphones><Mute command="True"></Mute></Microphones></Audio></Command>'
		answer=regex.search(self._putxml(request))
		self.status=answer.group(1)
		self.lastCommand="Mute"
		return self.status	

	def UnMute(self):
		
		regex=re.compile('<Command>.*status="(.+)".*')
		request='<Command><Audio><Microphones><Unmute command="True"></Unmute></Microphones></Audio></Command>'
		answer=regex.search(self._putxml(request))
		self.status=answer.group(1)
		self.lastCommand="UnMute"
		return self.status



if __name__=="__main__":

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



	codec1=codec()

	if options.mute:
		print codec1.Mute()
		
	if options.call:
		try:
			output=codec1.Dial(options.call) 
			print output
		except Exception:
			
			print output
 
	if options.disconnect:
		print codec1.DisconnectAll()
	if options.unmute:
		print codec1.UnMute()
  
