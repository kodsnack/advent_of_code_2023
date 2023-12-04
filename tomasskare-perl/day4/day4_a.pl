#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;

#my $inputfile = "example_a.txt";
my $inputfile = "input.txt";
open(my $fh, '<', $inputfile) || die "Unable to open file: $!";

my $sum = 0;
while(<$fh>){
    chomp;

    next unless(/^Card +(\d+): +([^|]+) +\| +(.*)$/);

    my $cardnr = $1;
    my $winlist = $2;
    my $ticketlist = $3;

    my %winnums = ();
    foreach my $winnr (split(/ +/, $winlist)) {
	$winnums{$winnr} = 1;
    }
    my $card_wins = 0;
    foreach my $ticketnr (split(/ +/, $ticketlist)) {
	next unless(defined($winnums{$ticketnr}));
	$card_wins++;
    }

    $sum += 2 ** ($card_wins - 1) if($card_wins);
}

close($fh);

print "sum: $sum\n";
