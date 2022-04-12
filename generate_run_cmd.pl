#!/usr/bin/perl
use strict;
use warnings;

sub resolve {
	my $addr = shift(@_);
	my $ip = `nslookup $addr | egrep Address | tail -n 1 | awk '{print \$2}'`; chomp $ip;
	return $ip;
}

my $RAC = "192.168.41.237:50000";
my @peers = ("crdt-bft-1","crdt-bft-2","crdt-bft-3","crdt-bft-4","crdt-bft-5");

my $leader = $peers[0];
print "Leader is $leader, which is the first of the peers\n";

my $i = 0;
foreach my $peer (@peers) {
	my $peer_addr = resolve($peer);
	my $leader_addr = resolve($leader);
	if($peer eq $leader) {
		$leader_addr = "this";
	}
	my $filename = "./run_$i.sh";
	open(FH, '>', $filename) or die $!;	
	print FH "node networkNode.js master full $peer_addr $leader_addr $RAC\n";
	close FH;
	`chmod +x $filename`;
	$i++;
}
