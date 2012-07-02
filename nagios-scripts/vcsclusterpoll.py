#!/usr/bin/env python
#coding: utf8
import re
import urllib2
import optparse
from urlparse import urlparse

class HTTPRealmFinderHandler(urllib2.HTTPBasicAuthHandler):
	def http_error_401(self, req, fp, code, msg, headers):
		realm_string = headers['www-authenticate']
		q1 = realm_string.find('"')
		q2 = realm_string.find('"', q1 + 1)
		realm = realm_string[q1 + 1:q2]
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

class vcsCluster():
	
	
	def __init__(ip,username,password):
		self.ip=ip
		self.username=username
		self.password=password
		self._vcsgetCluster()
		
	

	def _vcsgetCluster(self):
	
		URL = 'https://%s/resourceusage' % (ip)
		realm = HTTPRealmFinder(URL).prt()
		authHandler = urllib2.HTTPDigestAuthHandler()
		authHandler.add_password(realm, ip, username, password)
		urllib2.install_opener( urllib2.build_opener( authHandler ) )
		xmlRequest = urllib2.Request( URL )
		xmlRequest = urllib2.urlopen( xmlRequest )
	
		self.html= xmlRequest.read()


	def Nontraversal(self):
		html=self.html
		tmp1_start=html[html.find("Non-traversal call licenses"):]

		# Current

		regex=re.compile(".+Current<\/td><td><b>(\d+)</b><\/td>")
		self.nontraversal_current=regex.search(tmp1_start).group(1)

		# Peak

		regex=re.compile(".+Peak<\/td><td><b>(\d+)</b><\/td>")
		self.nontraversal_peak=regex.search(tmp1_start).group(1)


		# License limit
		regex=re.compile(".+License limit<\/td><td><b>(\d+)</b><\/td>")
		self.nontraversal_limit=regex.search(tmp1_start).group(1)

		self.nontraversal_percent=percent(self.nontraversal_current,self.nontraversal_limit)

	def Traversal(self):
		html=self.html
		tmp1_start=html[html.find("Traversal call licenses"):]

		# Current

		regex=re.compile(".+Current<\/td><td><b>(\d+)</b><\/td>")
		self.traversal_current=regex.search(tmp1_start).group(1)

		# Peak

		regex=re.compile(".+Peak<\/td><td><b>(\d+)</b><\/td>")
		self.traversal_peak=regex.search(tmp1_start).group(1)
		
		# License limit
		regex=re.compile(".+License limit<\/td><td><b>(\d+)</b><\/td>")
		self.traversal_limit=regex.search(tmp1_start).group(1)

		this.traversal_percent=self.percent(self.traversal_current,self.traversal_limit)
		
		
	def Registrations(self): 
		
		html=self.html
		tmp1_start=html[html.find("Registration licenses"):]

		# Current

		regex=re.compile(".+Current<\/td><td><b>(\d+)</b><\/td>")
		self.registration_current=regex.search(tmp1_start).group(1)

		# Peak

		regex=re.compile(".+Peak<\/td><td><b>(\d+)</b><\/td>")
		self.registration_peak=regex.search(tmp1_start).group(1)


		# License limit
		regex=re.compile(".+License limit<\/td><td><b>(\d+)</b><\/td>")
		self.registration_limit=regex.search(tmp1_start).group(1)
	
		# percent
		self.registration_percent=self.percent(self.registration_current,self.registration_limit)
		
		
	def percent(current,maximum):
		# <current> = current calls
		# <maximum> = maximum availabel calls
		
		
		return (int((float(current)/float(maximum)))*100.0)
		




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
p.add_option("-w", dest='warning', help='Warning level checks percent if % added to the end, if not it checks ports ')
p.add_option("-c", dest='critical', help='Critical level checks percent if % added to the end, if not it checks ports')

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

if options.critical is None:
	print '\n\nERROR    -c is manditory\n\n'
	p.print_help()
	exit(3)



try:
	client=vcsCluster(options.ip,options.username,options.password)

except urllib2.HTTPError as error:
	print error
	exit(-1)
	

def check(current,peak,limit,percent):
	#
	# Returns (int(exitcode),str(text))
	#
	
	text='current:%s max:%s licenses:%s percent:' % (current,peak,limit,percent)
	
	#  **** Critical check START ****
	if options.critical.find('%') !=-1:
		if int(percent) > int(options.critical):
			exitcode=int(2)
			return(exitcode,text)						
		
	if options.critical.find('%') ==-1:
		if int(current) > int(options.critical):
			exitcode=int(2)
			return(exitcode,text)
#  **** Critical check STOP ****
	
	
# **** Warning check START  ****
	if options.warning:
			# check if the percent sign is present in the warning option, if it is (find does not return -1)
			if options.warning.find('%') !=-1:
				
				if int(percent) > int(options.warning):
					exitcode=int(1)
					return(exitcode,text)
				
				else: 
					exitcode=int(0)
					return(exitcode,text)
				
			#if the percent sign is not present in the warning option don't check percent	
			if options.warning.find('%') ==-1:
				
				if int(current) > int(options.warning):
					exitcode=int(1)
					return(exitcode,text)
					
				else: 
					exitcode=int(0)
					return(exitcode,text)
			

# **** Warning check STOP  ****


if options.traversal:
	
	client.Traversal()
	(exitcode,text)=check(client.traversal_current,client.traversal_peak,client.traversal_limit,client.traversal_percent)
	print text
	exit(exitcode)
			
if options.nontraversal:
	
	client.Nontraversal()
	(exitcode,text)=check(client.nontraversal_current,client.nontraversal_peak,client.nontraversal_limit)
	print text
	exit(exitcode)

if options.registrations:
	
	client.Registrations()
	(exitcode,text)=check(client.registration_current,client.registration_peak,client.registration_limit)
	print text
	exit(exitcode)
