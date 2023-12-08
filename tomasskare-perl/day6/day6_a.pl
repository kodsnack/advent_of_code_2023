#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;

#my $inputfile = "example_a.txt";
my $inputfile = "input.txt";
open(my $fh, '<', $inputfile) || die "Unable to open file: $!";

# T = ts + tr;
# D < ts * tr;

my @times;
my @distances;
while(<$fh>){
    chomp;

    if(/^Time: +(.*)$/) {
	@times = split(/ +/, $1);
    } elsif(/^Distance: +(.*)$/) {
	@distances = split(/ +/, $1);
    }
}
close($fh);

my $sum = 1;
for(my $i = 0 ; $i < scalar @times ; $i++) {
    my $num_over = 0;
    for(my $ts = 1 ; $ts < $times[$i] ; $ts++) {
	$num_over++ if($ts * ($times[$i] - $ts) > $distances[$i]);
    }
    $sum *= $num_over if($num_over);
}

print "sum: $sum\n";
