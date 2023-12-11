#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;

#my $inputfile = "example_a1.txt";
#my $inputfile = "example_a2.txt";
my $inputfile = "input.txt";
open(my $fh, '<', $inputfile) || die "Unable to open file: $!";

my $pipes;
my $rows = 0;
my $sr;
my $sc;
while(<$fh>){
    chomp;

    my @row = split(//);
    $pipes->[$rows] = [@row];

    for(my $c = 0 ; $c < scalar @row ; $c++) {
	if($pipes->[$rows]->[$c] eq 'S') {
	    $sr = $rows;
	    $sc = $c;
	    last;
	}
    }

    $rows++;
}
close($fh);

my $cols = scalar @{$pipes->[0]};

#print Dumper($pipes);
#print "sr: $sr, sc: $sc\n";

my $turns = {'n' => {'|' => 'n',
		     '7' => 'w',
		     'F' => 'e'},
	     'e' => {'-' => 'e',
		     '7' => 's',
		     'J' => 'n'},
	     's' => {'|' => 's',
		     'J' => 'w',
		     'L' => 'e'},
	     'w' => {'-' => 'w',
		     'F' => 's',
		     'L' => 'n'}};

my $r1 = $sr;
my $c1 = $sc;
my $r2 = $sr;
my $c2 = $sc;
my $steps = 0;

# 'n', 'e', 's', 'w'
my $d1 = 'n';
my $d2 = 'w';
while($steps == 0 || $r1 != $r2 || $c1 != $c2) {
    my ($nr1, $nc1, $nd1, $nr2, $nc2, $nd2);

    ($nr1, $nc1, $nd1) = find_connecting_pipe($r1, $c1, $d1);
    if(!defined($nr1)) {
	$d1 = 'e';
	($nr1, $nc1, $nd1) = find_connecting_pipe($r1, $c1, $d1);
    }

#    print "step $steps: 1: (${r1}, ${c1}, $d1}) -> (${nr1}, ${nc1}, $nd1})\n";

    ($nr2, $nc2, $nd2) = find_connecting_pipe($r2, $c2, $d2);
    if(!defined($nr2)) {
	$d2 = 's';
	($nr2, $nc2, $nd2) = find_connecting_pipe($r2, $c2, $d2);
    }

#    print "step $steps: 2: (${r2}, ${c2}, $d2}) -> (${nr2}, ${nc2}, $nd2})\n";

    ($r1, $c1, $d1) = ($nr1, $nc1, $nd1);
    ($r2, $c2, $d2) = ($nr2, $nc2, $nd2);
    $steps++;
}

print "steps: $steps\n";

sub find_connecting_pipe {
    my ($r, $c, $d) = @_;
    my $nr = $r;
    my $nc = $c;

#    print "from (${r}, ${c}, $d})\n";
    if($d eq 'n') {
	return (undef, undef, undef) if($r == 0);
	$nr = $r - 1;
    } elsif($d eq 'e') {
	return (undef, undef, undef) if($c == $cols);
	$nc = $c + 1;
    } elsif($d eq 's') {
	return (undef, undef, undef) if($r == $rows);
	$nr = $r + 1;
    } elsif($d eq 'w') {
	return (undef, undef, undef) if($c == 0);
	$nc = $c - 1;
    }

    my $np = $pipes->[$nr]->[$nc];
    my $nd = $turns->{$d}->{$np};

#    print "check (${nr}, ${nc}, ${nd})\n";

    return (undef, undef, undef) if(!defined($nd));
    return ($nr, $nc, $nd);
}
