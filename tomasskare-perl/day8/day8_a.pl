#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;

#my $inputfile = "example_a.txt";
#my $inputfile = "example_a2.txt";
my $inputfile = "input.txt";
open(my $fh, '<', $inputfile) || die "Unable to open file: $!";

my $first = 1;
my @steps;
my $map = {};
while(<$fh>){
    chomp;

    if($first) {
	@steps = split(//);
	$first = 0;
    } elsif(/([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)/) {
	$map->{$1}->{'L'} = $2;
	$map->{$1}->{'R'} = $3;
    }

}
close($fh);

my $pos = "AAA";
my $num = 0;
Outer_Loop:
while(1) {
    foreach my $step (@steps) {
	last Outer_Loop if($pos eq "ZZZ");
	die "What? pos=$pos, step=$step" if(!defined($map->{$pos}->{$step}));
	$pos = $map->{$pos}->{$step};
	$num++;
    }
}

print "num: $num\n";
