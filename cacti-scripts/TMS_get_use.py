import urllib2
import sys
import re
import optparse



# Start option parsing
p = optparse.OptionParser()
p.add_option('-i',dest="ip",metavar="<address>",help='address to vcs, ip or dns name')
p.add_option('-u',dest="username",metavar="<username>",help='Username for the vcs' )
p.add_option("-p", dest="password",metavar="<Password>",help='Password for the vcs')
p.add_option('--movi',dest='movi',metavar='',help='gets the movi licenses from tms and prints it in a cacti friendly way',action="store_const", const=1)
p.add_option('--system',dest='system',metavar='',help='Gets the system licenses from tms and prints it in a cacti friendly way',action="store_const", const=1)

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

if options.movi !=None and options.system !=None:
	print "You have to make a choice man, you can't choose to show both the movi and the system licenses..."
	p.print_help()
	exit(-1)

# Stop options parsing

net_address=options.ip

# Authentication

password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
top_level_url = "http://" +net_address+"/tms/default.aspx?pageId=35"
password_mgr.add_password(None, top_level_url, options.username, options.password)
handler = urllib2.HTTPBasicAuthHandler(password_mgr)
opener = urllib2.build_opener(handler)
opener.open(top_level_url)
urllib2.install_opener(opener)
response = urllib2.urlopen(top_level_url)
html = response.read()


#################################
#	Available Movi Licenses:
##################################

# the regex
regex=re.compile('ctl00_uxContent_ctl01_uxTotalMoviLicenses">(\d+)')

# narrow it down to the available movi licenses field
html2=html[html.find('ctl00_uxContent_ctl01_uxTotalMoviLicenses'):]
html3=html2[:html2.find('</span>')]

# extracts the data and puts it in a var
svar=regex.search(html3)
total_movi_lic=svar.group(1)



#################################
#	Total Movi Licenses:
#################################

# the regex
regex=re.compile('ctl00_uxContent_ctl01_uxAvailableMoviLicenses">(\d+)')

# narrow it down to the available movi licenses field
html2=html[html.find('ctl00_uxContent_ctl01_uxAvailableMoviLicenses'):]
html3=html2[:html2.find('</span>')]

# extracts the data and puts it in a var
svar=regex.search(html3)
avail_movi_lic=svar.group(1)


#################################
#	Total System Licenses:
#################################

# the regex
regex=re.compile('ctl00_uxContent_ctl01_uxTotalSystemLicenses">(\d+)')

# narrow it down to the available movi licenses field
html2=html[html.find('ctl00_uxContent_ctl01_uxTotalSystemLicenses'):]
html3=html2[:html2.find('</span>')]

# extracts the data and puts it in a var
svar=regex.search(html3)
total_system_lic=svar.group(1)



#################################
#	Available System Licenses:
#################################

# the regex
regex=re.compile('ctl00_uxContent_ctl01_uxAvailableSystemLicenses">(\d+)')

# narrow it down to the available movi licenses field
html2=html[html.find('ctl00_uxContent_ctl01_uxAvailableSystemLicenses'):]
html3=html2[:html2.find('</span>')]

# extracts the data and puts it in a var
svar=regex.search(html3)
avail_system_lic=svar.group(1)




if options.movi is not None:

	print "Avail:%s Total:%s Use:%i" %(avail_movi_lic,total_movi_lic,(int(total_movi_lic)-int(avail_movi_lic)))
	exit(0)

if options.system is not None:
		print "Avail:%s Total:%s Use:%i" %(avail_system_lic,total_system_lic,(int(total_system_lic)-int(avail_system_lic)))
