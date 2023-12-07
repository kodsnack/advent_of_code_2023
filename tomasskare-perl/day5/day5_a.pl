#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;

#my $inputfile = "example_a.txt";
my $inputfile = "input.txt";
open(my $fh, '<', $inputfile) || die "Unable to open file: $!";

my %seeds;
my @seed_to_soil_map;
my @soil_to_fertilizer_map;
my @fertilizer_to_water_map;
my @water_to_light_map;
my @light_to_temperature_map;
my @temperature_to_humidity_map;
my @humidity_to_location_map;
my $curr_arr;
while(<$fh>){
    chomp;

    if(/^seeds: (.*)$/) {
	foreach my $seed (split(/ +/, $1)) {
	    $seeds{$seed} = 1;
	}
    } elsif(/^seed-to-soil map:/) {
	$curr_arr = \@seed_to_soil_map;
    } elsif(/^soil-to-fertilizer map:/) {
	$curr_arr = \@soil_to_fertilizer_map;
    } elsif(/^fertilizer-to-water map:/) {
	$curr_arr = \@fertilizer_to_water_map;
    } elsif(/^water-to-light map:/) {
	$curr_arr = \@water_to_light_map;
    } elsif(/^light-to-temperature map:/) {
	$curr_arr = \@light_to_temperature_map;
    } elsif(/^temperature-to-humidity map:/) {
	$curr_arr = \@temperature_to_humidity_map;
    } elsif(/^humidity-to-location map:/) {
	$curr_arr = \@humidity_to_location_map;
    } elsif(/^(\d+) +(\d+) +(\d+)/) {
	my $h = {'dst_first' => $1,
		 'dst_last' => $1 + $3 - 1,
		 'src_first' => $2,
		 'src_last' => $2 + $3 - 1,
		 'length' => $3};
	push @$curr_arr, $h;
    }

}

#print Dumper(\%seeds);
#print Dumper(\@seed_to_soil_map);
#print Dumper(\@soil_to_fertilizer_map);
#print Dumper(\@fertilizer_to_water_map);
#print Dumper(\@water_to_light_map);
#print Dumper(\@light_to_temperature_map);
#print Dumper(\@temperature_to_humidity_map);
#print Dumper(\@humidity_to_location_map);

close($fh);

my $min_location;
foreach my $seed (keys %seeds) {
    my $value = $seed;
  arr_loop:
    foreach my $map_arr (\@seed_to_soil_map,
			 \@soil_to_fertilizer_map,
			 \@fertilizer_to_water_map,
			 \@water_to_light_map,
			 \@light_to_temperature_map,
			 \@temperature_to_humidity_map,
			 \@humidity_to_location_map) {
	foreach my $map (@$map_arr) {
	    next if($value < $map->{'src_first'} ||
		    $value > $map->{'src_last'});
	    $value = $value - $map->{'src_first'} + $map->{'dst_first'};
	    next arr_loop;
	}
    }

    $min_location = $value if(!defined($min_location) || $value < $min_location);
}

print "min_location: $min_location\n";
