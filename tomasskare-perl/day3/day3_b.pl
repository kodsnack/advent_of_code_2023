#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;

#my $inputfile = "example_a.txt";
my $inputfile = "input.txt";
open(my $fh, '<', $inputfile) || die "Unable to open file: $!";

my $m = [];
my $numrows = 0;
my $numcols = 0;
while(<$fh>){
    chomp;

    $numcols = 0;
    foreach my $c (split(//)) {
	$m->[$numrows]->[$numcols] = $c;
	$numcols++;
    }
    $numrows++;
}

#print Dumper($m);

close($fh);

my $sum = 0;

for(my $r = 0 ; $r < $numrows ; $r++) {
    for(my $c = 0 ; $c < $numcols ; $c++) {
	next if($m->[$r]->[$c] =~ /[0-9.]/);
	next unless($m->[$r]->[$c] eq '*');

	my $gears = {};
	if($r > 0 && $c > 0 && $m->[$r - 1]->[$c - 1] =~ /[0-9]/) {
	    # nw
	    check_pos($gears, $r - 1, $c - 1);
	}
	if($r > 0 && $m->[$r - 1]->[$c] =~ /[0-9]/) {
	    # n
	    check_pos($gears, $r - 1, $c);
	}
	if($r > 0 && $c < $numcols && $m->[$r - 1]->[$c + 1] =~ /[0-9]/) {
	    # ne
	    check_pos($gears, $r - 1, $c + 1);
	}
	if($c < $numcols && $m->[$r]->[$c + 1] =~ /[0-9]/) {
	    # e
	    check_pos($gears, $r, $c + 1);
	}
	if($r < $numrows && $c < $numcols && $m->[$r + 1]->[$c + 1] =~ /[0-9]/) {
	    # se
	    check_pos($gears, $r + 1, $c + 1);
	}
	if($r < $numrows && $m->[$r + 1]->[$c] =~ /[0-9]/) {
	    # s
	    check_pos($gears, $r + 1, $c);
	}
	if($r < $numrows && $c > 0 && $m->[$r + 1]->[$c - 1] =~ /[0-9]/) {
	    # sw
	    check_pos($gears, $r + 1, $c - 1);
	}
	if($c > 0 && $m->[$r]->[$c - 1] =~ /[0-9]/) {
	    # w
	    check_pos($gears, $r, $c - 1);
	}

#	print "r: $r, c: $c, gears: " . Dumper($gears) . "\n";

	next if(scalar(keys %{$gears}) != 2);

	my $total = 1;
	foreach my $g (keys %{$gears}) {
	    $total *= $gears->{$g};
	}
	$sum += $total;
    }
}

print "sum: $sum\n";


sub check_pos {
    my ($gears, $sr, $sc) = @_;

#    print "sr: $sr, sc: $sc, m: " . $m->[$sr]->[$sc] . "\n";
    while($sc > 0 && $m->[$sr]->[$sc - 1] =~ /[0-9]/) {
	$sc--;
    }

    my $num = 0;
    my $ssc = $sc;
    while($ssc < $numcols && $m->[$sr]->[$ssc] =~ /[0-9]/) {
	$num = $num * 10 + $m->[$sr]->[$ssc];
	$ssc++;
    }

#    print "sr: $sr, sc: $sc, num: $num\n";

    $gears->{"${sr}_${sc}"} = $num;
}
