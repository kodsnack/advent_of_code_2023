#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;

#my $inputfile = "example_a.txt";
my $inputfile = "input.txt";
open(my $fh, '<', $inputfile) || die "Unable to open file: $!";

my $games = {};

while(<$fh>){
    chomp;

    next unless(/^Game ([0-9]+): (.*)$/);
    my $gamenr = $1;
    foreach (split(/; /, $2)) {
	foreach (split(/, /)) {
	    next unless(/^([0-9]+) (.*)$/);
	    my $amount = $1;
	    my $color = $2;
	    if(!defined($games->{$gamenr}->{$color}) ||
	       $games->{$gamenr}->{$color} < $amount) {
		$games->{$gamenr}->{$color} = $amount;
	    }
	}
    }
}

my $sum = 0;
foreach my $gamenr (keys %{$games}) {
    next if(defined($games->{$gamenr}->{'red'}) &&
	    $games->{$gamenr}->{'red'} > 12);
    next if(defined($games->{$gamenr}->{'green'}) &&
	    $games->{$gamenr}->{'green'} > 13);
    next if(defined($games->{$gamenr}->{'blue'}) &&
	    $games->{$gamenr}->{'blue'} > 14);

    $sum += $gamenr;
}

print "sum: $sum\n";

close($fh);
