
#/bin/usr/python
from twisted.internet.protocol import Factory, Protocol,ClientFactory
from twisted.internet import reactor
from datetime import datetime

'''

Sends a OPTION Request to 5060 and checks if it gets a 200 OK back

'''



def uri_parse(uri):
    #
    return uri.split("@")


def generate_branch():
    # Generates a semi random branch id
    # [*] Needs to be fixed to give a real random string
    #


    import random
    length=13
    magic_number="z9hG4bK"

    branch=magic_number
    salt=list('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM123456789')
    x=0 
    while (x <length):    
        branch=branch + random.choice(salt)
        x +=1   
    return branch


class SIP(Protocol):

    def __init__(self,factory):
        self.factory=factory


         
        

    def connectionLost(self, reason):   
        pass
   

    def send_options(self):
        import random
        
        #self.status=random.getrandbits(128)

        self.branch=generate_branch()
        self.callid=random.getrandbits(128)
        connection=point.transport.getHost().__dict__
        uri=self.factory.uri
        remote_uri=self.factory.remote_uri
    
        
        sip_header="OPTIONS sip:{};transport=TCP SIP/2.0\r\n".format(self.factory.uri)
        
        sip_header+="Max-Forwards: 20\r\n"
        sip_header+="From: <sip:{};transport=TCP>\r\n".format(uri)
        sip_header+="To: <sip:{};transport=TCP>\r\n".format(remote_uri)
        sip_header+="Call-ID: {}\r\n".format(self.callid)
        sip_header+="CSeq: 20 OPTIONS\r\n"
        sip_header+='Contact: <sip:{}@{}:{};transport=TCP>\r\n'.format(uri_parse(uri)[0],connection['host'],connection['port'])
        sip_header+="Accept: application/sdp\r\n"
        sip_header+="Content-Length: 0\r\n"
        sip_header+="\r\n"
        
        
        self.transport.write(sip_header)
        


    def connectionMade(self):
         
            self.send_options()
            


    def dataReceived(self,data):
        import re
        if data.startswith("SIP/2.0 200 OK"):
            self.factory.status=0
            self.transport.loseConnection()
        else:    
        
            self.factory.status=2
            self.transport.loseConnection()
            


     


class SIPFactory(ClientFactory):
    def __init__(self):
        self.bindAddress=()
    
    def startedConnecting(self,connector):
        pass

    def buildProtocol(self,addr):
        return SIP(self)

    def clientConnectionFailed(self,connector,reason):
        reactor.stop()  

    def clientConnectionLost(self,connector,reason):
        reactor.stop()
        
       






import optparse 

p = optparse.OptionParser()
p.add_option('-i',dest="ip",metavar="<address>",help='Adress to SIP Server')
p.add_option('-a',dest="address",metavar="<address>",help='your URI' )
p.add_option("-r",dest="remote_address",metavar="<Redirect>",help='remote URI')
options, arguments = p.parse_args()



if options.ip is None or options.address is None or options.remote_address is None:
    print '\n\nERROR -i -a and -r is manditory\n\n'
    p.print_help()
    exit(-1)



fact=SIPFactory()
point=reactor.connectTCP(options.ip,5060,fact)
fact.uri=options.address
fact.remote_uri=options.remote_address
fact.status=0
reactor.run()

if fact.status==0:
    print "OK"
else:
    print "Connection Error"
exit(fact.status)
