#!/usr/bin/perl
#
# Simple command line utility ; checks SRV records for SIP and H.323 




#
# Moduler
#
use Net::DNS; # For DNS resolving 

use Getopt::Std; # for kommandolinje argumenter


#
#Globale Variabler
#
my $sip,$h323,$e164;

my $dns1;  
my $dns2;


getopt('dnth');  






#sjekker hvilken dns-leverandør som er valgt
if ($opt_d eq "OpenDNS"){
  $dns1="208.67.222.222";
  $dns2="208.67.220.220"; 
 
}
if ($opt_d eq 'GoogleDNS'){
  $dns1="8.8.8.8";
  $dns2="8.8.4.4"; 
 
}

if ($opt_d eq 'DNSAdvantage'){
  $dns1="156.154.70.1";
  $dns2="156.154.71.1"; 
 
}

# default dns servere.
if (!$opt_d){
  $dns1="8.8.8.8";
  $dns2="8.8.4.4"; 
}

#
#usage hvis det ikke har kommet noen optioner eller -h
#

if ((!$opt_n && !$ARGV[0])||$opt_h ){
usage();
exit(0);
}



#
# Man har muligeheten til å bare skrive domenenavnet som argument
#

if ($ARGV[0] && !$opt_n){
print "\nH.323 Records:\n";
printsrv($ARGV[0],'_h323ls._udp.',$dns1,$dns2);
printsrv($ARGV[0],'_h323ls._tcp.',$dns1,$dns2);
printsrv($ARGV[0],'_h323cs._udp.',$dns1,$dns2);
printsrv($ARGV[0],'_h323cs._tcp.',$dns1,$dns2);
printsrv($ARGV[0],'_h323ls._udp.',$dns1,$dns2);
print "\nSIP Records:\n";
printsrv($ARGV[0],'_sip._udp.',$dns1,$dns2);
printsrv($ARGV[0],'_sip._tcp.',$dns1,$dns2);
printsrv($ARGV[0],'_sips._udp.',$dns1,$dns2);
printsrv($ARGV[0],'_sips._tcp.',$dns1,$dns2);
print"\n";
exit(0);


}


#
#
#

if (!$opt_t ){
print "\nH.323 Records:\n";
printsrv($opt_n,'_h323ls._udp.',$dns1,$dns2);
printsrv($opt_n,'_h323ls._tcp.',$dns1,$dns2);
printsrv($opt_n,'_h323cs._udp.',$dns1,$dns2);
printsrv($opt_n,'_h323cs._tcp.',$dns1,$dns2);
printsrv($opt_n,'_h323ls._udp.',$dns1,$dns2);
print "\nSIP Records:\n";
printsrv($opt_n,'_sip._udp.',$dns1,$dns2);
printsrv($opt_n,'_sip._tcp.',$dns1,$dns2);
printsrv($opt_n,'_sips._udp.',$dns1,$dns2);
printsrv($opt_n,'_sips._tcp.',$dns1,$dns2);
print"\n";
exit(0);
}

if ($opt_t){
printsrv($opt_n,$opt_t,$dns1,$dns2);


}


sub usage(){

	print "\nUSAGE: program [-d DNSserver][-n domain] [-t SRV record] [-h] domain
	[-d] DNS servers options: OpenDNS, GoogleDNS, DNSAdvantage
	[-n] Domain to check SRV record
        [-t] specify SRV record, if omitted H323 and SIP records are scanned
	[-h] This help
	\n";
}


sub printsrv{
my ($domain, $type,$domain1,$domain2)=($_[0],$_[1],$_[2],$_[3]);


my $res   = Net::DNS::Resolver->new(nameserver =>["$domain1","$domain2"]);
my $domaintype="$type"."$domain";
my $query = $res->search($domaintype."", "SRV" );
my $counter;
  if ($query) {
   
   foreach my $rr ($query->answer) {
          
          next unless $rr->type eq "SRV";
          $counter=$counter+1;
           print "Record:$domaintype, Pri:".$rr->priority.", Weight: ".$rr->weight.", Port: ".$rr->port.", Target: ".$rr->target." \n";
		}
  } else {
     # warn "query failed: ", $res->errorstring, "\n";
  }
return $counter;
}

