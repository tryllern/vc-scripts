#!/usr/bin/env python
#coding: utf8 
import urllib2
import optparse
from urlparse import urlparse
from xml.dom.minidom import parseString


'''
	Class to get the REALM from the header.
	eks:

	realm=HTTPRealmFinder('http://e1.viju.vc/getxml?')
	realm.prt()

	stolen from http://code.activestate.com/recipes/267197-urllib2-for-actions-depending-on-http-response-cod/


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
def vcsgetxml(ip,username,password,request):
	URL = 'https://%s/%s' % (ip,request)
	realm=HTTPRealmFinder(URL)
	realm=realm.prt()
	ah = urllib2.HTTPDigestAuthHandler()
	ah.add_password(realm,ip,username,password)
	urllib2.install_opener(urllib2.build_opener(ah))
	r = urllib2.Request(URL)
	obj = urllib2.urlopen(r)
	return obj.read()





def vcsgetTraversalCalls(ip,username,password):
	'''
	   Returns a tulip (current,max,total)
	
	'''
	url='getxml?location=/Status/ResourceUsage/Calls/Traversal'
	xmlResponse= vcsgetxml(ip,username,password,url)
	#return xmlResponse
	dom = parseString(xmlResponse)
	Current=  dom.getElementsByTagName('Current')[0]._get_firstChild().toprettyxml().rstrip()
	Max= dom.getElementsByTagName('Max')[0]._get_firstChild().toprettyxml().rstrip()
	Total=dom.getElementsByTagName('Total')[0]._get_firstChild().toprettyxml().rstrip()
	return (Current,Max,Total)
def vcsgetNonTraversalCalls(ip,username,password):
	'''
	   Returns a tulip (current,max,total)
	
	'''
	url='getxml?location=/Status/ResourceUsage/Calls/NonTraversal'
	xmlResponse= vcsgetxml(ip,username,password,url)
	#return xmlResponse
	dom = parseString(xmlResponse)
	Current=  dom.getElementsByTagName('Current')[0]._get_firstChild().toprettyxml().rstrip()
	Max= dom.getElementsByTagName('Max')[0]._get_firstChild().toprettyxml().rstrip()
	Total=dom.getElementsByTagName('Total')[0]._get_firstChild().toprettyxml().rstrip()
	return (Current,Max,Total)
def vcsgetRegistrations(ip,username,password):
	'''
	   Returns a tulip (current,max,total)
	
	'''
	url='getxml?location=/Status/ResourceUsage/Registrations'
	xmlResponse= vcsgetxml(ip,username,password,url)
	#return xmlResponse
	dom = parseString(xmlResponse)
	Current=  dom.getElementsByTagName('Current')[0]._get_firstChild().toprettyxml().rstrip()
	Max= dom.getElementsByTagName('Max')[0]._get_firstChild().toprettyxml().rstrip()
	Total=dom.getElementsByTagName('Total')[0]._get_firstChild().toprettyxml().rstrip()
	return (Current,Max,Total)
def vcsgetTURN(ip,username,password):
	'''
	   Returns a tulip (current,max,total)
	
	'''
	url='getxml?location=/Status/ResourceUsage/TURN/Relays'
	xmlResponse= vcsgetxml(ip,username,password,url)
	#return xmlResponse
	dom = parseString(xmlResponse)
	Current=  dom.getElementsByTagName('Current')[0]._get_firstChild().toprettyxml().rstrip()
	Max= dom.getElementsByTagName('Max')[0]._get_firstChild().toprettyxml().rstrip()
	Total=dom.getElementsByTagName('Total')[0]._get_firstChild().toprettyxml().rstrip()
	return (Current,Max,Total)
def vcsgetUptime(ip,username,password):
	'''
	Uptime: <Time in seconds>
	'''
	
	url='getxml?location=/Status/SystemUnit/Uptime'
	xmlResponse= vcsgetxml(ip,username,password,url)
	dom = parseString(xmlResponse)
	uptime=dom.getElementsByTagName('Uptime')[0]._get_firstChild().toprettyxml().rstrip()
	return uptime

def vcsgetCallLicenses(ip,username,password):
	'''
	Returns a tuple of Nontraversal,traversal,registration
	'''
	
	url='getxml?location=/Status/SystemUnit/Software/Configuration'
	resp= vcsgetxml(ip,username,password,url)
	
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
p.add_option("--turn",dest='turn',help='Gets TURN info',action="store_const", const=1)
p.add_option("--uptime",dest='uptime',help='Gets uptime from vcs',action="store_const", const=1)
options, arguments = p.parse_args()

if len(arguments) >= 1:
  p.error("incorrect number of arguments")
'''
End of commando lin eoptions check
'''

'''
Check if -i -u -p is commited
'''
if options.ip is None:
	print '\n\nERROR    -i is manditory\n\n'
	p.print_help()
	exit(-1)
if options.username is None:
	print '\n\nERROR    -u is manditory\n\n'
	p.print_help()
	exit(-1)
if options.password is None:
	print '\n\nERROR    -p is manditory\n\n'
	p.print_help()
	exit(-1)

(licenses_nontrav,licenses_trav,licenses_reg)=vcsgetCallLicenses(options.ip,options.username,options.password)

if options.traversal:
	(current,max,total)=vcsgetTraversalCalls(options.ip,options.username,options.password)
	print 'current:%s max:%s total:%s licenses:%s' % (current,max,total,licenses_trav)
	
if options.nontraversal:
	
	(current,max,total)=vcsgetNonTraversalCalls(options.ip,options.username,options.password)
	print 'current:%s max:%s total:%s licenses:%s' % (current,max,total,licenses_nontrav)
	
if options.turn:
	(current,max,total)=vcsgetTURN(options.ip,options.username,options.password)
	print 'current:%s max:%s total:%s' % (current,max,total)
if options.registrations:
	(current,max,total)=vcsgetRegistrations(options.ip,options.username,options.password)
	print 'current:%s max:%s total:%s licenses:%s' % (current,max,total,licneses_reg)

if options.uptime:
	uptime=vcsgetUptime(options.ip,options.username,options.password)
	print uptime
