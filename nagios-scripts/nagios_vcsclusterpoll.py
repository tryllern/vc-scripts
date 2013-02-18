#!/usr/bin/env python
#coding: utf8
import re
import urllib2
import optparse
import mechanize
import cookielib
#from urlparse import urlparse



class vcsCluster():
	
	
	def __init__(self,ip,username,password):
		self.ip=ip
		self.username=username
		self.password=password
		self._vcsgetCluster()
		
	

	def _vcsgetCluster(self):
	
		URL = 'https://%s/login' % (self.ip)
		cj=cookielib.LWPCookieJar()

		mech = mechanize.Browser()
		#mech.set_debug_http(True)
                mech.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
                mech.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time=1 )

                
                mech.set_cookiejar(cj)
                mech.set_handle_redirect(True)
                mech.set_handle_robots(False)
                mech.set_handle_referer(True)
                mech.open(URL)
		mech.select_form(nr=1)
		mech["username"] = self.username
		mech["password"] = self.password
	        mech.submit().read()
		
		URL='https://%s/resourceusage' % (self.ip)
		self.html=mech.open(URL).read()
		


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
                
                #Percent
		self.nontraversal_percent=self.percent(
                        self.nontraversal_current,self.nontraversal_limit
                        )

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
                # Percent
                self.traversal_percent=self.percent(self.traversal_current,self.traversal_limit)
		
		
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
		self.registration_percent=self.percent( 
                        self.registration_current, self.registration_limit
                        )
		
		
	def percent(self,current,maximum):
		# <current> = current calls
		# <maximum> = maximum availabel calls
		
                if  int(current)==0 :
		    return 0
                
                else:
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
	
	text='current:%s max:%s licenses:%s percent:%s' % (str(current),
                str(peak),str(limit),str(percent))
	
	#  **** Critical check START ****
	if options.critical.find('%') !=-1:
		if int(percent) > int(options.critical):
			exitcode=int(2)
			return(exitcode,text)	

        else:
        #if options.critical.find('%') ==-1:
		if int(current) > int(options.critical):
			exitcode=int(2)
			return(exitcode,text)
#  **** Critical check STOP ****
	
	
# **** Warning check START  ****
	if options.warning:
	    # check if the percent sign is present in the warning option, 
            #if it is (find does not return -1)
	    if options.warning.find('%') !=-1:
				
		if int(percent) > int(options.warning):
			exitcode=int(1)
			return(exitcode,text)
				
		else: 
			exitcode=int(0)
			return(exitcode,text)
				
			#if the percent sign is not present in the warning 
                        #option don't check percent	
		if options.warning.find('%') ==-1:
		
		    if int(current) > int(options.warning):
			exitcode=int(1)
			return(exitcode,text)
					
		else: 
		    exitcode=int(0)
		    return(exitcode,text)
			

#if all else fails...
        return (0,text)


# **** Warning check STOP  ****

exitcode=0
text=''

if options.traversal:
	
	client.Traversal()
        (exitcode,text)=check(client.traversal_current,
                client.traversal_peak,client.traversal_limit,
                client.traversal_percent)
	print text
	exit(exitcode)
			
if options.nontraversal:
	
	client.Nontraversal()
        (exitcode,text)=check(client.nontraversal_current,
                 client.nontraversal_peak, 
                client.nontraversal_limit, 
                client.nontraversal_percent )
	print text
	exit(exitcode)

if options.registrations:
	
	client.Registrations()
	(exitcode,text)=check( client.registration_current, 
                client.registration_peak, 
                client.registration_limit ,client.registration_percent)
	print text
	exit(exitcode)
