#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;

#my $inputfile = "example_a.txt";
my $inputfile = "input.txt";
open(my $fh, '<', $inputfile) || die "Unable to open file: $!";

# T = ts + tr;
# D < ts * tr;

my $time;
my $distance;
while(<$fh>){
    chomp;

    if(/^Time: +(.*)$/) {
	$time = $1;
	$time =~ s/ +//g;
    } elsif(/^Distance: +(.*)$/) {
	$distance = $1;
	$distance =~ s/ +//g;
    }
}
close($fh);

print "time: $time, distance: $distance\n";

my $first_time = 0;
for(my $ts = 1 ; $ts < $time ; $ts++) {
    if($ts * ($time - $ts) > $distance) {
	$first_time = $ts;
	last;
    }
}

my $half_time = int($time / 2);
my $total_time_over = 2 * ($half_time - $first_time) + 1;
print "total_time_over: $total_time_over\n";
