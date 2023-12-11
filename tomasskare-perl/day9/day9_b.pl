#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;

#my $inputfile = "example_a.txt";
my $inputfile = "input.txt";
open(my $fh, '<', $inputfile) || die "Unable to open file: $!";

my $seqs = [];
my $s = 0;
while(<$fh>){
    chomp;

    $seqs->[$s]->[0] = [split(/ +/)];
    $s++;
}
close($fh);

#print STDERR Dumper($seqs);

my $sum = 0;
for($s = 0 ; $s < scalar @$seqs ; $s++) {
    my $di = 0;
    my $all_zeroes = 0;
    while(!$all_zeroes) {
	$all_zeroes = 1;
	for(my $i = 0 ; $i < scalar @{$seqs->[$s]->[$di]} - 1 ; $i++) {
	    my $diff = $seqs->[$s]->[$di]->[$i + 1] - $seqs->[$s]->[$di]->[$i];
	    push @{$seqs->[$s]->[$di + 1]}, $diff;
	    $all_zeroes = 0 if($diff != 0);
	}
	$di++;
    }

    my $diff = 0;
    while($di > 0) {
	unshift @{$seqs->[$s]->[$di]}, $diff;
	$diff = $seqs->[$s]->[$di - 1]->[0] - $diff;
	$di--;
    }

    $sum += $diff;
}

print "sum: $sum\n";
