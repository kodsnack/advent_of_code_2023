#!/usr/bin/perl

use strict;
use warnings;

#my $inputfile = "example_b.txt";
my $inputfile = "input.txt";
open(my $fh, '<', $inputfile) || die "Unable to open file: $!";

my $sum = 0;

while(<$fh>){
    chomp;
    my $line = lc($_);
    my $first;
    my $last;

    my $inword = "";
    foreach my $a (split("", $line)) {
	if($a =~ /[a-z]/) {
	    $inword .= $a;
	    $inword =~ s/one/1/;
	    $inword =~ s/two/2/;
	    $inword =~ s/three/3/;
	    $inword =~ s/four/4/;
	    $inword =~ s/five/5/;
	    $inword =~ s/six/6/;
	    $inword =~ s/seven/7/;
	    $inword =~ s/eight/8/;
	    $inword =~ s/nine/9/;
	    $inword =~ s/.*([0-9]).*/$1/;
	    if($inword =~ /^[0-9]$/) {
		$a = $inword;
		$inword = "";
	    }
	}

	next unless($a =~ /[0-9]/);

	$inword = "";

	if(!defined($first)) {
	    $first = $a;
	    last
	}
    }

    $inword = "";
    foreach my $a (reverse split("", $line)) {
	if($a =~ /[a-z]/) {
	    $inword = $a . $inword;
	    $inword =~ s/one/1/;
	    $inword =~ s/two/2/;
	    $inword =~ s/three/3/;
	    $inword =~ s/four/4/;
	    $inword =~ s/five/5/;
	    $inword =~ s/six/6/;
	    $inword =~ s/seven/7/;
	    $inword =~ s/eight/8/;
	    $inword =~ s/nine/9/;
	    $inword =~ s/.*([0-9]).*/$1/;
	    if($inword =~ /^[0-9]$/) {
		$a = $inword;
		$inword = "";
	    }
	}

	next unless($a =~ /[0-9]/);

	$inword = "";

	if(!defined($last)) {
	    $last = $a;
	    last
	}
    }

    my $linesum = $first . $last;
    $sum += $linesum;
}

print "sum: $sum\n";

close($fh);
