import urllib2
from xml.dom.minidom import parseString
import optparse	
import string
#coding: utf8 


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

#   *************************   START TextFormatter *********************************

left  = 0
center = centre = 1
right  = 2

class TextFormatter:

    """
    Formats text into columns.

    Constructor takes a list of dictionaries that each specify the
    properties for a column. Dictionary entries can be:

       width         the width within which the text will be wrapped
       alignment     left|center|right
       margin        amount of space to prefix in front of column

    The compose() method takes a list of strings and returns a formatted
    string consisting of each string wrapped within its respective column.

    Example:

            formatter = TextFormatter(
                    (
                            {'width': 10},
                            {'width': 12, 'margin': 4},
                            {'width': 20, 'margin': 8, 'alignment': right},
                    )
            )

            print formatter.compose(
                    (
                            "A rather short paragraph",
                            "Here is a paragraph containing a veryveryverylongwordindeed.",
                            "And now for something on the right-hand side.",
                    )
            )

    gives:

            A rather      Here is a                    And now for
            short         paragraph               something on the
            paragraph     containing a            right-hand side.
                                      veryveryvery
                                      longwordinde
                                      ed.

    """
    class Column:

        def __init__(self, width=75, alignment=left, margin=0, fill=1, pad=1):
            self.width = width
            self.alignment = alignment
            self.margin = margin
            self.fill = fill
            self.pad = pad
            self.lines = []

        def align(self, line):
            if self.alignment == center:
                return string.center(line, self.width)
            elif self.alignment == right:
                return string.rjust(line, self.width)
            else:
                if self.pad:
                    return string.ljust(line, self.width)
                else:
                    return line

        def wrap(self, text):
            self.lines = []
            words = []
            if self.fill:               # SKWM
                for word in string.split(text):
                    wordlen = len(word)
                    if wordlen <= self.width:  # fixed MRM
                        words.append(word)
                    else:
                        for i in range(0, wordlen, self.width):
                            words.append(word[i:i+self.width])
            else:
                for line in string.split(text,'\n'):
                    for word in string.split(line):
                        for i in range(0, len(word), self.width):
                            words.append(word[i:i+self.width])
                    words.append('\n')
                if words[-1] == '\n': words.pop() # remove trailing newline - this comment by MRM

            if words:
                current = words.pop(0)
                for word in words:
                    increment = 1 + len(word)
                    if word == '\n':
                        self.lines.append(self.align(current))
                        current = ''
                    elif len(current) + increment > self.width:
                        self.lines.append(self.align(current))
                        current = word
                    else:
                        if current:
                            current = current + ' ' + word
                        else:
                            current = word
                if current: self.lines.append(self.align(current))

        def getline(self, index):
            if index < len(self.lines):
                return ' '*self.margin + self.lines[index]
            else:
                if self.pad:
                    return ' ' * (self.margin + self.width)
                else:
                    return ''

        def numlines(self):
            return len(self.lines)

    def __init__(self, colspeclist):
        self.columns = []
        for colspec in colspeclist:
            self.columns.append(apply(TextFormatter.Column, (), colspec))

    def compose(self, textlist):
        numlines = 0
        textlist = list(textlist)
        if len(textlist) != len(self.columns):
            raise IndexError, "Number of text items does not match columns"
        for text, column in map(None, textlist, self.columns):
            column.wrap(text)
            numlines = max(numlines, column.numlines())
        complines = [''] * numlines
        for ln in range(numlines):
            for column in self.columns:
                complines[ln] = complines[ln] + column.getline(ln)
        return string.join(complines, '\n') 
        #return string.join(complines, '\n')+ '\n' if you want spaces between lines

#*****************************END TextFormatter **************************************************

# Start ; from tandbergAPI-file
def findRealm(ip,username,password,request):
	
  '''
  Finds the realm string when authentication fails, used to log into vcs
  '''
  theurl='http://%s/getxml?location=' % ip
 
  passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
  passman.add_password(None, theurl, username, password)
  authhandler = urllib2.HTTPBasicAuthHandler(passman)
  opener = urllib2.build_opener(authhandler)
  urllib2.install_opener(opener)
  try:
	
	answer= urllib2.urlopen(theurl + urllib2.quote(request))
	return answer.read()
	
  except urllib2.HTTPError,e:
	realm_string=e.headers.get('www-authenticate', '')
	q1 = realm_string.find('"')
	q2 = realm_string.find('"', q1+1)
	realm = realm_string[q1+1:q2]
	return realm
def vcsgetxml(ip,username,password,request):
	
    
 	URL = 'http://%s/getxml?location=%s' % (ip,request)
	
	realm=findRealm(ip,username,password,request)
	
	ah = urllib2.HTTPDigestAuthHandler()
	ah.add_password(realm,ip,username,password)
	urllib2.install_opener(urllib2.build_opener(ah))
	r = urllib2.Request(URL)
	obj = urllib2.urlopen(r)
	return obj.read()
def vcsgetActiveCalls(ip,username,password):
    url='/Status/Calls'
    resp= vcsgetxml(ip,username,password,url)
    dom = parseString(resp)
    return dom
# Stop; from tandbergAPI-file


print "Protocol:   State:     Duration: 	   Starttime: 						From:  						To:"
print "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"


def getcalls(xml,counter):
 active_calls=counter
 for calls in dom.getElementsByTagName('Call'):
	active_calls=active_calls+1
	Protocol=calls.getElementsByTagName('Protocol')[0].toprettyxml().split('\n')[1][1:]
	duration=calls.getElementsByTagName('Duration')[0].toprettyxml().split('\n')[1][1:]
	state=calls.getElementsByTagName('State')[0].toprettyxml().split('\n')[1][1:]
	starttime=calls.getElementsByTagName('StartTime')[0].toprettyxml().split('\n')[1][1:]
	
	if Protocol == 'H323':
			step1=calls.getElementsByTagName('H323')[0]
			step2=step1.getElementsByTagName('Alias')[0]
			callingfrom=step1.getElementsByTagName('Value')[0].toprettyxml().split('\n')[1][1:]
	if Protocol == 'SIP':
			step1=calls.getElementsByTagName('SIP')[0]
			step2=step1.getElementsByTagName('Alias')[0]
			callingfrom=step1.getElementsByTagName('Value')[0].toprettyxml().split('\n')[1][1:]
	
	target_step1=calls.getElementsByTagName('Target')[0]
	target=target_step1.getElementsByTagName('Value')[0].toprettyxml().split('\n')[1][1:]
	
	

	#line="%s %s %s %s %s %s" % (Protocol,state,duration,starttime,callingfrom,target.lstrip()) 
	#print ' '.join(('%*s' % (25, 1) for i in line.split()))


	import string
	left  = 0
	center = centre = 1
	right  = 2

	formatter = TextFormatter(
            (
                    {'width': 6},
                    {'width': 12, 'margin': 4, 'fill': 0},
                    {'width': 8, 'margin': 4, 'fill': 0},
                    {'width': 20, 'margin': 4, 'fill': 0},
                    {'width': 49, 'margin': 8, 'alignment': right},
                    {'width': 49, 'margin': 8, 'alignment': right}											
            )
	)

	result = formatter.compose(
            (
                   Protocol,state,duration,starttime,callingfrom,target
                    
                    
            )
    )

	
	print result
 return active_calls	


dom =vcsgetActiveCalls(options.ip,options.username,options.password )
active_calls=0

active_calls=getcalls(dom,active_calls)

print "-------------------"
print "| Active Calls:%s |" % active_calls	 
print "-------------------"



