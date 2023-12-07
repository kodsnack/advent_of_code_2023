#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;

#my $inputfile = "example_own.txt";
#my $inputfile = "example_a.txt";
my $inputfile = "input.txt";
open(my $fh, '<', $inputfile) || die "Unable to open file: $!";

my %hands;
while(<$fh>){
    chomp;

    next unless(/^([AKQJT2-9]{5}) +(\d+)$/);
    my $hand = $1;
    my $bid = $2;

    $hands{$hand} = $bid;
}
close($fh);

my @sorted_hands = sort hand_cmp keys %hands;
#print "sorted: " . Dumper(@sorted_hands);
my $rank = 1;
my $sum = 0;
foreach my $hand (@sorted_hands) {
#    print "hand: $hand, rank: $rank, bid: " . $hands{$hand} . "\n";
    $sum += $rank * $hands{$hand};
    $rank++;
}

print "sum: $sum\n";

sub hand_cmp {
    our ($a, $b);

    my $a_type = find_type_wildcard($a);
    my $b_type = find_type_wildcard($b);

    return -1 if($a_type < $b_type);
    return 1 if($a_type > $b_type);

    for(my $i = 0 ; $i < 5 ; $i++) {
	my $s = card_cmp(substr($a, $i, 1), substr($b, $i, 1));
	return $s unless($s == 0);
    }

    return 0;
}

sub find_type_wildcard {
    my ($hand) = @_;

    my $max = 0;
    foreach my $replace ('2', '3', '4', '5', '6', '7', '8', '9',
			 'T', 'Q', 'K', 'A') {
	my $testhand = $hand;
	$testhand =~ s/J/$replace/g;
	my $type = find_type($testhand);
	$max = $type if($type > $max);
    }

    return $max;
}

sub find_type {
    my ($hand) = @_;

    my $sorted = join("", sort split(//, $hand));
    return 6 if($sorted =~ /^(.)\g1{4}$/);
    return 5 if($sorted =~ /^(.)\g1{3}.$/);
    return 5 if($sorted =~ /^.(.)\g1{3}$/);
    return 4 if($sorted =~ /^(.)\g1{1}(.)\g2{2}$/);
    return 4 if($sorted =~ /^(.)\g1{2}(.)\g2{1}$/);
    return 3 if($sorted =~ /^(.)\g1{2}..$/);
    return 3 if($sorted =~ /^.(.)\g1{2}.$/);
    return 3 if($sorted =~ /^..(.)\g1{2}$/);
    return 2 if($sorted =~ /^(.)\g1(.)\g2.$/);
    return 2 if($sorted =~ /^.(.)\g1(.)\g2$/);
    return 2 if($sorted =~ /^(.)\g1.(.)\g2$/);
    return 1 if($sorted =~ /^(.)\g1...$/);
    return 1 if($sorted =~ /^.(.)\g1..$/);
    return 1 if($sorted =~ /^..(.)\g1.$/);
    return 1 if($sorted =~ /^...(.)\g1$/);
    return 0;
}

sub card_cmp {
    my ($a, $b) = @_;

    return 0 if($a eq $b);

    foreach my $t ('A', 'K', 'Q', 'T') {
	return 1 if($a eq $t);
	return -1 if($b eq $t);
    }

    $a =~ s/J/1/;
    $b =~ s/J/1/;

    return -1 if($a < $b);
    return 1 if($a > $b);

    return 0;
}
