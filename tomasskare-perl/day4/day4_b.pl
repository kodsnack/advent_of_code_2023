#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;

#my $inputfile = "example_a.txt";
my $inputfile = "input.txt";
open(my $fh, '<', $inputfile) || die "Unable to open file: $!";

my @cards = (0);

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

    my $mul = ($cards[$cardnr] // 0) + 1;
#    print "cardnr $cardnr, card_wins $card_wins, mul $mul\n";
    $cards[$cardnr]++;
    for(my $c = 1 ; $c <= $card_wins ; $c++) {
	$cards[$cardnr + $c] += $mul;
    }
#    print Dumper(@cards);
}

close($fh);

#print Dumper(@cards);

my $sum = 0;
foreach my $card_num (@cards) {
    $sum += $card_num if($card_num);
}

print "sum: $sum\n";
