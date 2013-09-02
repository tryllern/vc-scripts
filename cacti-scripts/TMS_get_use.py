import urllib2
import sys
import re
import optparse


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


net_address=options.ip

password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
top_level_url = "http://" +net_address+"/tms/default.aspx?pageId=35"
password_mgr.add_password(None, top_level_url, options.username, options.password)
handler = urllib2.HTTPBasicAuthHandler(password_mgr)
opener = urllib2.build_opener(handler)
opener.open(top_level_url)
urllib2.install_opener(opener)
response = urllib2.urlopen(top_level_url)
html = response.read()


if options.movi is not None:
    regex=re.compile('<span id="ctl00_uxContent_ctl01_uxTotalProvisioningLicenses" class="textbox">(\d+)</span>')
    total_movi_lic=regex.search(html).group(1)
    
    regex=re.compile('<span id="ctl00_uxContent_ctl01_uxAvailableProvisioningLicenses" class="textbox">(\d+)</span>')
    avail_movi_lic=regex.search(html).group(1)

    print "Avail:%s Total:%s Use:%i" %(avail_movi_lic,total_movi_lic,(int(total_movi_lic)-int(avail_movi_lic)))
    exit(0)

if options.system is not None:
    regex=re.compile('<span id="ctl00_uxContent_ctl01_uxTotalSystemLicenses" class="textbox">(\d+)</span>')
    total_system_lic=regex.search(html).group(1)

    regex=re.compile('<span id="ctl00_uxContent_ctl01_uxAvailableSystemLicenses" class="textbox">(\d+)</span>')
    avail_system_lic=regex.search(html).group(1)
            
    print "Avail:%s Total:%s Use:%i" %(avail_system_lic,total_system_lic,(int(total_system_lic)-int(avail_system_lic)))
    exit(0)
