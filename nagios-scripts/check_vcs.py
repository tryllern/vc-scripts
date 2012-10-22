#!/usr/bin/env python
#coding: utf8 
import urllib2
import optparse
from urlparse import urlparse
from xml.dom.minidom import parseString


'''
Nagios script for VCS

exit codes

0 - Ok
1 - warning
2 - critical
3 - unknown

Warning 
Critical - manditory

'''
	
class HTTPRealmFinderHandler(urllib2.HTTPBasicAuthHandler):
			def http_error_401(self, req, fp, code, msg, headers):
				realm_string = headers['www-authenticate']
        
				q1 = realm_string.find('"')
				q2 = realm_string.find('"', q1+1)
				realm = realm_string[q1+1:q2]
        
				self.realm = realm
class HTTPRealmFinder:

			def __init__(self, url):
				self.url = url
				scheme, domain, path, x1, x2, x3 = urlparse(url)
        
				handler = HTTPRealmFinderHandler()
				handler.add_password(None, domain, 'foo', 'bar')
				self.handler = handler
        
				opener = urllib2.build_opener(handler)
				urllib2.install_opener(opener)

			def ping(self, url):
				try:
					urllib2.urlopen(url)
				except urllib2.HTTPError, e:
					pass

			def get(self):
				self.ping(self.url)
				try:
					realm = self.handler.realm
				except AttributeError:
					realm = None
        
				return realm

			def prt(self):
				return self.get()

def vcsgetxml(ip,username,password,request,proto='http'):
	
	if proto=='https':
		URL = 'https://%s/%s' % (ip,request)
		realm=HTTPRealmFinder(URL)
		realm=realm.prt()
		ah = urllib2.HTTPBasicAuthHandler()
	if proto=='http':
		URL = 'http://%s/%s' % (ip,request)
		realm=HTTPRealmFinder(URL)
		realm=realm.prt()
		ah = urllib2.HTTPDigestAuthHandler()
		
	ah.add_password(realm,ip,username,password)
	urllib2.install_opener(urllib2.build_opener(ah))
	r = urllib2.Request(URL)
	obj = urllib2.urlopen(r)
	return obj.read()

def vcsgetTraversalCalls(ip,username,password,proto='http'):
	'''
	   Returns a tulip (current,max,total)
	
	'''
	url='getxml?location=/Status/ResourceUsage/Calls/Traversal'
	xmlResponse= vcsgetxml(ip,username,password,url,proto)
	#return xmlResponse
	dom = parseString(xmlResponse)
	Current=  dom.getElementsByTagName('Current')[0]._get_firstChild().toprettyxml().rstrip()
	Max= dom.getElementsByTagName('Max')[0]._get_firstChild().toprettyxml().rstrip()
	Total=dom.getElementsByTagName('Total')[0]._get_firstChild().toprettyxml().rstrip()
	return (Current,Max,Total)
def vcsgetNonTraversalCalls(ip,username,password,proto='http'):
	'''
	   Returns a tulip (current,max,total)
	
	'''
	url='getxml?location=/Status/ResourceUsage/Calls/NonTraversal'
	xmlResponse= vcsgetxml(ip,username,password,url,proto)
	
	dom = parseString(xmlResponse)
	Current=  dom.getElementsByTagName('Current')[0]._get_firstChild().toprettyxml().rstrip()
	Max= dom.getElementsByTagName('Max')[0]._get_firstChild().toprettyxml().rstrip()
	Total=dom.getElementsByTagName('Total')[0]._get_firstChild().toprettyxml().rstrip()
	return (Current,Max,Total)
def vcsgetRegistrations(ip,username,password,proto='http'):
	'''
	   Returns a tulip (current,max,total)
	
	'''
	url='getxml?location=/Status/ResourceUsage/Registrations'
	xmlResponse= vcsgetxml(ip,username,password,url,proto)
	
	dom = parseString(xmlResponse)
	Current=  dom.getElementsByTagName('Current')[0]._get_firstChild().toprettyxml().rstrip()
	Max= dom.getElementsByTagName('Max')[0]._get_firstChild().toprettyxml().rstrip()
	Total=dom.getElementsByTagName('Total')[0]._get_firstChild().toprettyxml().rstrip()
	return (Current,Max,Total)
def vcsgetTURN(ip,username,password,proto='http'):
	'''
	   Returns a tulip (current,max,total)
	
	'''
	url='getxml?location=/Status/ResourceUsage/TURN/Relays'
	xmlResponse= vcsgetxml(ip,username,password,url,proto)
	
	dom = parseString(xmlResponse)
	Current=  dom.getElementsByTagName('Current')[0]._get_firstChild().toprettyxml().rstrip()
	Max= dom.getElementsByTagName('Max')[0]._get_firstChild().toprettyxml().rstrip()
	Total=dom.getElementsByTagName('Total')[0]._get_firstChild().toprettyxml().rstrip()
	return (Current,Max,Total)
def vcsgetUptime(ip,username,password,proto='http'):
	'''
	Uptime: <Time in seconds>
	'''
	
	url='getxml?location=/Status/SystemUnit/Uptime'
	xmlResponse= vcsgetxml(ip,username,password,url,proto)
	dom = parseString(xmlResponse)
	uptime=dom.getElementsByTagName('Uptime')[0]._get_firstChild().toprettyxml().rstrip()
	return uptime
def vcsgetCallLicenses(ip,username,password,proto='http'):
	'''
	Returns a tuple of Nontraversal,traversal,registration
	'''
	
	url='getxml?location=/Status/SystemUnit/Software/Configuration'
	resp= vcsgetxml(ip,username,password,url,proto)
	
	dom = parseString(resp)
	Nontraversal= dom.getElementsByTagName('NonTraversalCalls')[0]._get_firstChild().toprettyxml().rstrip()
	Traversal=dom.getElementsByTagName('TraversalCalls')[0]._get_firstChild().toprettyxml().rstrip()
	Registrations=dom.getElementsByTagName('Registrations')[0]._get_firstChild().toprettyxml().rstrip()
	
	return (Nontraversal,Traversal,Registrations)



'''
checking command line options
'''
p = optparse.OptionParser()
p.add_option('-i',dest="ip",metavar="<address>",help='address to vcs, ip or dns name')
p.add_option('-u',dest="username",metavar="<username>",help='Username for the vcs'	)
p.add_option("-p", dest="password",metavar="<Password>",help='Password for the vcs')
p.add_option("--traversal",dest='traversal',help='Get Traversal calls Info',action="store_const", const=1)
p.add_option("--nontraversal",dest='nontraversal',help='Get Non Traversal calls Info',action="store_const", const=1)
p.add_option("--registrations",dest="registrations",help="Get Registrations info",action="store_const", const=1)
p.add_option("-w",dest='warning',help='Warning level')
p.add_option("-c",dest='critical',help='Critical level')
p.add_option("-s",dest="secure",help="Use https, default is http",action="store_const", const=1)
options, arguments = p.parse_args()

if len(arguments) >= 1:
  p.error("incorrect number of arguments")
'''
End of commando lin option check
'''
'''
Check if -i -u -p is commited
'''
if options.ip is None:
	print '\n\nERROR    -i is manditory\n\n'
	p.print_help()
	exit(3)
if options.username is None:
	print '\n\nERROR    -u is manditory\n\n'
	p.print_help()
	exit(3)
if options.password is None:
	print '\n\nERROR    -p is manditory\n\n'
	p.print_help()
	exit(3)
if options.critical is None:
	print '\n\nERROR    -c is manditory\n\n'
	p.print_help()
	exit(3)


if options.secure:
	proto='https'
else:
	proto='http'

(licenses_nontrav,licenses_trav,licenses_reg)=vcsgetCallLicenses(options.ip,options.username,options.password,proto)

#
# if the warning options is not defined, set it as the same as critical
#

if not options.warning: options.warning=options.critical


if options.traversal:
      import math
      
      (current,max,total)=vcsgetTraversalCalls(options.ip,options.username,options.password,proto)
      percent=(float(current)/float(licenses_trav))*100.0
      percent=int(percent)
      if percent > int(options.critical):  
        print "traversal calls:%s percent of %s in use " % (percent,licenses_trav)
        exit(2)
      if options.warning :  
    	
    	if percent  >= int(options.warning):
    		print "traversal calls:%s percent of %s in use " % (percent,licenses_trav)
    		exit(1)
    	else:
			print "traversal calls:%s percent of %s in use " % (percent,licenses_trav)
    	exit(0)	
    	
      else: 
    	print "traversal calls:%s percent of %s in use " % (percent,licenses_trav)
    	exit(0)	

if options.nontraversal:
      import math
      
      (current,max,total)=vcsgetNonTraversalCalls(options.ip,options.username,options.password,proto)
      percent=(float(current)/float(licenses_nontrav))*100.0
      percent=int(percent)
      if percent > int(options.critical): 
        print "Nontraversal calls:%s percent of %s in use " % (percent,licenses_nontrav)
        exit(2)
      if options.warning :
    	
        if percent  >= int(options.warning):
    		print "Nontraversal calls:%s percent of %s in use " % (percent,licenses_nontrav)
    		exit(1)
        else:
			print "Nontraversal calls:%s percent of %s in use " % (percent,licenses_nontrav)
			exit(0)	
    	
      else: 
    	print "Nontraversal calls:%s percent of %s in use " % (percent,licenses_nontrav)
    	exit(0)	
				
if options.registrations:
      import math
      
      (current,max,total)=vcsgetRegistrations(options.ip,options.username,options.password,proto)
      percent=(float(current)/float(licenses_reg))*100.0
      percent=int(percent)
      if percent > int(options.critical): 
        print "Registrations calls:%s percent of %s in use " % (percent,licenses_reg)
        exit(2)
      if options.warning :
    	
        if percent  >= int(options.warning):
    		print "Registrations calls:%s percent of %s in use " % (percent,licenses_reg)
    		exit(1)
        else:
			print "Registrations calls:%s percent of %s in use " % (percent,licenses_reg)
			exit(0)	
    	
      else: 
    	print "Registrations calls:%s percent of %s in use " % (percent,licenses_reg)
    	exit(0)	
	
exit(3)
