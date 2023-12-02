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
    my $red = $games->{$gamenr}->{'red'} // 0;
    my $green = $games->{$gamenr}->{'green'} // 0;
    my $blue = $games->{$gamenr}->{'blue'} // 0;

    my $power = $red * $green * $blue;

    $sum += $power;
}

print "sum: $sum\n";

close($fh);
