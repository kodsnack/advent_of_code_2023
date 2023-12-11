#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;

#my $inputfile = "example_a.txt";
my $inputfile = "input.txt";
open(my $fh, '<', $inputfile) || die "Unable to open file: $!";

my $ogalaxies = {};
my $gnum = 1;
my $rows = 0;
my $cols = 0;
while(<$fh>){
    chomp;

    my @row = split(//);
    $cols = scalar @row;

    my $any_g = 0;
    for(my $c = 0 ; $c < $cols ; $c++) {
	next if($row[$c] eq '.');

	$ogalaxies->{$c}->{$rows} = $gnum++;
	$any_g = 1;
    }

    $rows++ if(!$any_g);
    $rows++;
}
close($fh);

my $galaxies = {};
my $gmap = {};
my $add_c = 0;
for(my $c = 0 ; $c < $cols ; $c++) {
    if(scalar keys %{$ogalaxies->{$c}} == 0) {
	$add_c++;
	next;
    }

    foreach my $r (keys %{$ogalaxies->{$c}}) {
	my $g = $ogalaxies->{$c}->{$r};
	$galaxies->{$c + $add_c}->{$r} = $g;
	$gmap->{$g} = [$c + $add_c, $r];
    }
}

$cols += $add_c;

my $len = 0;
for(my $g1 = 1 ; $g1 < $gnum ; $g1++) {
    for(my $g2 = 1 ; $g2 < $g1 ; $g2++) {
	my ($c1, $r1) = @{$gmap->{$g1}};
	my ($c2, $r2) = @{$gmap->{$g2}};
	$len += abs($c2 - $c1) + abs($r2 - $r1);
    }
}

print "len: $len\n";

