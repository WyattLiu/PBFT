#!/usr/bin/perl
use strict;
use warnings;

my @servers = ("192.168.41.237:3002","192.168.41.100:3002","192.168.41.76:3002","192.168.41.161:3002","192.168.41.248:3002");

my $num_client = 1;
my $i = 0;
while($i < $num_client) {
	foreach my $server (@servers) {
		print "Schedule $i to $server\n";
		`cat ./workload_template.json | sed 's/FILLTHIS/$server/g' > ./parallel_client_$i.json`;
		$i++;
		if($i == $num_client) {
			last;
		}
	}
}

$i = 0;
my @children;
while($i < $num_client) {
	my $pid = fork();
	if($pid == 0) {
		print "run python3 benchmark.py ./parallel_client_$i.json\n";
		`python3 benchmark.py ./parallel_client_$i.json > ./parallel_client_$i.result`;
	       	exit;	
	} else {
		push @children, $pid;
	}
	$i++
}

foreach my $child (@children) {
	waitpid($child,0);
}

my @results = `cat ./parallel_client_*.result | egrep -a Throughput -A 1`;
print @results;
