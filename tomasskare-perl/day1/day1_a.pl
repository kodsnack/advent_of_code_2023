#!/usr/bin/perl

use strict;
use warnings;

#my $inputfile = "example_a.txt";
my $inputfile = "input.txt";
open(my $fh, '<', $inputfile) || die "Unable to open file: $!";

my $sum = 0;

while(<$fh>){
    chomp;
    my $line = $_;
    my $first = undef;
    my $last = undef;

    foreach my $a (split("",$line)) {
	next unless($a =~ /[0-9]/);
	if(!defined($first)) {
	    $first = $last = $a;
	} else {
	    $last = $a;
	}
    }

    my $linesum = $first . $last;
    $sum += $linesum;
}

print "sum: $sum\n";

close($fh);
