#!/usr/bin/perl
use strict;
use warnings;

my $RAC = "192.168.1.104:50000";
my @peers = ("wyatt-performance","wyatt-xperformance");

my $leader = $peers[0];
print "Leader is $leader, which is the first of the peers\n";

my $i = 0;
foreach my $peer (@peers) {
	my $leader_addr = $leader;
	if($peer eq $leader) {
		$leader_addr = "this";
	}
	my $filename = "./run_$i.sh";
	open(FH, '>', $filename) or die $!;	
	print FH "node networkNode.js master full $peer $leader_addr $RAC\n";
	close FH;
	`chmod +x $filename`;
	$i++;
}
