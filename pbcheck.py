# post xml soap message
#
# Gets/checks phonebook for system from Tandberg TMS

import sys, httplib
import optparse	
p = optparse.OptionParser()
p.add_option('--mac','-m',dest="macid",metavar="<MAC Address>")
p.add_option("--server", "-s", dest="server",metavar="<TMS SERVER>")
options, arguments = p.parse_args()

SoapMessage="""<?xml version="1.0" encoding="utf-8"?>
<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
xmlns="http://www.tandberg.net/2004/06/PhoneBookSearch/">
<env:Body xmlns="http://www.tandberg.net/2004/06/PhoneBookSearch/">
<Search>
<Identification>
<MACAddress>%s</MACAddress>
</Identification>
</Search>
</env:Body>
</env:Envelope>
""" % options.macid

webservice = httplib.HTTP(options.server) 
webservice.putrequest("POST", "/tms/public/external/phonebook/phonebookservice.asmx?")
webservice.putheader("Host", options.server) 
webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
webservice.putheader("Content-length", "%d" % len(SoapMessage))
webservice.putheader("SOAPAction", "http://www.tandberg.net/2004/06/PhoneBookSearch/Search")
webservice.endheaders()
webservice.send(SoapMessage)

statuscode, statusmessage, header = webservice.getreply()
res = webservice.getfile().read()
print res,"\n"
