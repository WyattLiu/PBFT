#!/usr/bin/perl
use strict;
use warnings;

my $i = 1;

while($i <=5) {
	my @a = `rsync -avzhe  ssh ./PBFT crdt-bft-$i:~/`;
	print @a;
	my @b = `rsync -avzhe  ssh ./rKVCRDT crdt-bft-$i:~/`;
	print @b;
	$i++;
}

my $bin = "/home/ubuntu/rKVCRDT/RAC/bin/Debug/net5.0/Project_RAC";

