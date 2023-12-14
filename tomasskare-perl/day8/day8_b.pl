#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;
use Math::Utils qw(lcm);

#my $inputfile = "example_b.txt";
my $inputfile = "input.txt";
open(my $fh, '<', $inputfile) || die "Unable to open file: $!";

my $first = 1;
my @steps;
my @positions;
my $map = {};
while(<$fh>){
    chomp;

    if($first) {
	@steps = split(//);
	$first = 0;
    } elsif(/([0-9A-Z]{3}) = \(([0-9A-Z]{3}), ([0-9A-Z]{3})\)/) {
	$map->{$1}->{'L'} = $2;
	$map->{$1}->{'R'} = $3;
	my $start = $1;
	push @positions, $start if($start =~ /..A/);
    }

}
close($fh);

my @nums;
for(my $p = 0 ; $p < scalar @positions ; $p++) {
    my $num = 0;
  Outer_Loop:
    while(1) {
	foreach my $step (@steps) {
	    last Outer_Loop if($positions[$p] =~ /..Z/);
	    $positions[$p] = $map->{$positions[$p]}->{$step};
	    $num++;
	}
  }
    $nums[$p] = $num;
}

my $min_steps = lcm(@nums);
print "num steps: $min_steps\n";
