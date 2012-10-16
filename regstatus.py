#!/usr/bin/env python

import urllib2
from xml.dom.minidom import parseString
import optparse	
import string
#coding: utf8 

def getxml(ip,username,password,request):
  
  theurl='http://%s/getxml?location=' % ip
 
  passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
  passman.add_password(None, theurl, username, password)
  authhandler = urllib2.HTTPBasicAuthHandler(passman)
  opener = urllib2.build_opener(authhandler)
  urllib2.install_opener(opener)
  answer= urllib2.urlopen(theurl + urllib2.quote(request))
  return answer.read()
def getXMLtagvalue(xmlfile,tagname):
	'''
	returns one xml value
	'''
	xmlvalue=xmlfile.getElementsByTagName(tagname)[0].toprettyxml().split('\n')[1][1:]
	return xmlvalue
def getXMLslice(xmlfile,tagname):
	'''
	returns a slice of  xml
	'''
	xmlslice=xmlfile.getElementsByTagName(tagname)[0]
	return xmlslice
	
	
def getProductId(ip,username,password):
	'''
     Description:  
		Gets the product id - a string identifying what kind of system the codec is eksampel: TANDBERG CODEC 3000MXP
		used by the findCodecPlattform function to find out what kind of plattform the codec is running on.
		This function supports all the plattforms(te,tc and mxp)
     Parameters:
			ip - 		the ip adress of the codec
			username -	username, usally 'admin'
			password - 	password, on te/tc plattform the default is <blank> on MXP its 'TANDBERG'
  
	 Dependencies:
			getxml() 
  
	'''
	request="/Status/SystemUnit/ProductId"
	xmlAnswer=getxml(ip,username,password,request)
	Start=xmlAnswer.find('<ProductId')+20
	Stop=xmlAnswer.find('</ProductId')
	return xmlAnswer[Start:Stop]
def findCodecPlattform(ip,username,password):
        '''
     Description:  
			finds out what kind of plattform the codec is running on, returns either the string 'te','tc' or 'mxp'
			should also return 'unknown' for unknown systems.
			This function supports all the plattforms(te,tc and mxp)
     Parameters:
			ip - 		the ip adress of the codec
			username -	username, usally 'admin'
			password - 	password, on te/tc plattform the default is <blank> on MXP its 'TANDBERG'
  
	 Dependencies:
			getxml() 
			getProductID()
    '''	
	   
	softid=getProductId(ip,username,password)
	systemDict= {
		'TANDBERG Edge 75MXP': 'mxp',
		'TANDBERG Edge 85MXP': 'mxp',
		'TANDBERG Edge 95MXP': 'mxp',
		'TANDBERG 1700MXP': 'mxp',
		'TANDBERG 6000MXP': 'mxp',
		'TANDBERG 3000MXP': 'mxp',
		'TANDBERG 990MXP': 'mxp',
		'TANDBERG 880MXP': 'mxp',
		'TANDBERG CODEC 3000MXP': 'mxp',
		'TANDBERG CODEC 6000MXP': 'mxp',
		'TANDBERG Profile 3000MXP': 'mxp',
		'TANDBERG Profile 6000MXP': 'mxp',
		'TANDBERG Codec C20': 'tc',
		'TANDBERG Codec C40': 'tc',
		'TANDBERG Codec C60': 'tc',
		'TANDBERG Codec C90': 'tc',
		'TANDBERG Profile 42 C40': 'tc',
		'TANDBERG Profile 52 C40': 'tc',
		'TANDBERG Profile 52 Dual': 'tc',
		'TANDBERG T1': 'tc',
		'TANDBERG EX60': 'tc',
		'TANDBERG EX90': 'tc',
		'TANDBERG E20': 'te'
	
	}
	
	return systemDict[softid]

def tcgetSIPregistrationStatus(ip,username,password):
	'''
	Tested on E20 TE4.0.0.246968
	Returns registration status to proxy
	'''
	resp=getxml(ip,username,password,'/Status/SIP/Registration/Status')
	dom=parseString(resp)
	
	return  getXMLtagvalue(getXMLslice(dom,'Status'),'Status')
def tcgetH323registrationStatus(ip,username,password):
	'''
	Tested on E20 TE4.0.0.246968
	Returns registration status to proxy
	'''
	resp=getxml(ip,username,password,'/Status/H323/Gatekeeper/Status')
	dom=parseString(resp)
	
	return  getXMLtagvalue(getXMLslice(dom,'Status'),'Status')
def mxpgetSIPregistrationStatus(ip,username,password):
	'''
	Tested on E20 TE4.0.0.246968
	Returns registration status to proxy
	'''
	resp=getxml(ip,username,password,'/Status/SIP/Registration')
	dom=parseString(resp)
	return dom.getElementsByTagName('Registration')[0].toxml()[31:].split('\n')[0][:-2]
	
def mxpgetH323registrationStatus(ip,username,password):
	'''
	Tested on E20 TE4.0.0.246968
	Returns registration status to proxy
	'''
	resp=getxml(ip,username,password,'/Status/H323Gatekeeper')
	dom=parseString(resp)
	return dom.getElementsByTagName('H323Gatekeeper')[0].toxml()[33:].split('\n')[0][:-2]

# Start option parsing
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


# Stop options parsing




plattform=findCodecPlattform(options.ip,options.username,options.password)


if plattform == 'mxp':
	
	Status_h323=str(mxpgetH323registrationStatus(options.ip,options.username,options.password))
	Status_sip=str(mxpgetSIPregistrationStatus(options.ip,options.username,options.password))

if plattform == 'tc' :
	
	Status_h323=str(tcgetH323registrationStatus(options.ip,options.username,options.password))
	Status_sip=str(tcgetSIPregistrationStatus(options.ip,options.username,options.password))

if plattform == 'te':
	Status_h323='Inactive'
	Status_sip=str(tcgetSIPregistrationStatus(options.ip,options.username,options.password))

if Status_h323=='Failed' and Status_sip=='Failed':
	print "Exit code 2 for %s  h323:%s  sip:%s" % (options.ip,Status_h323,Status_sip)
	
	exit(2)

if Status_h323=='Failed' or Status_sip=='Failed':
	if Status_h323=='Inactive' and Status_sip=='Failed':
		print "Exit code 2 for %s  h323:%s  sip:%s" % (options.ip,Status_h323,Status_sip)
		exit(2)
	
	if Status_h323=='Failed' and Status_sip=='Inactive':
		print "Exit code 2 for %s  h323:%s  sip:%s" % (options.ip,Status_h323,Status_sip)
		exit(2)
	
	print "Exit code 1 for %s  h323:%s  sip:%s" % (options.ip,Status_h323,Status_sip)
	exit(1)


if Status_h323=='Registered' or Status_sip=='Registered':
	print "Exit code 0 for %s  h323:%s  sip:%s" % (options.ip,Status_h323,Status_sip)
	
	exit(0)
else:
	print "Exit code 1 for %s  h323:%s  sip:%s" % (options.ip,Status_h323,Status_sip)
	
	exit(1)
