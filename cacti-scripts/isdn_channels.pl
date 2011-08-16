#!/usr/bin/perl
#
# returns active isdn channels on TANDBERG ISDN GATEWAY
# 
#
require RPC::XML::Client;


#
# Brukernavn og passord og ip-adr hentes fra kommandolinja
#
my $user=shift;
my $password=shift;
my $addr=shift;


$cli = RPC::XML::Client->new('http://'.$addr.'/RPC2');

$options = RPC::XML::struct->new(
'authenticationUser' => $user,
'authenticationPassword' => $password,
'port' => 0); # sender brukernavn,passord og isdn portnummer som option

$resp = $cli->simple_request('isdn.port.query',$options); # xml-request

#

for ($i=0;$i<=30;$i++){
$test=$test + $resp->{'bChannels'}->[$i]->{'active'}; # går igjennom alle kanalene og plusser sammen linjene som er i bruk.
}

print "active:".$test; 
