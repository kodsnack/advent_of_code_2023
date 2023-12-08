#!/usr/bin/perl

use strict;
use warnings;
use List::Util 'pairs';
use Data::Dumper;

#my $inputfile = "example_a.txt";
my $inputfile = "input.txt";
open(my $fh, '<', $inputfile) || die "Unable to open file: $!";

my @seeds_list;
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
	my $seedlist = $1;
	while($seedlist =~ /(\d+) +(\d+) */g) {
	    my $h = {'dst_first' => int($1),
		     'dst_last' => $1 + $2 - 1};
	    push @seeds_list, $h;
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
	my $h = {'dst_first' => int($1),
		 'dst_last' => $1 + $3 - 1,
		 'src_first' => int($2),
		 'src_last' => $2 + $3 - 1,
		 'length' => int($3)};
	push @$curr_arr, $h;
    }

}

#print Dumper(\@seeds_list);
#print Dumper(\@seed_to_soil_map);
#print Dumper(\@soil_to_fertilizer_map);
#print Dumper(\@fertilizer_to_water_map);
#print Dumper(\@water_to_light_map);
#print Dumper(\@light_to_temperature_map);
#print Dumper(\@temperature_to_humidity_map);
#print Dumper(\@humidity_to_location_map);

close($fh);

my $valuelist = \@seeds_list;
foreach my $pair (pairs ("seed-to-soil", \@seed_to_soil_map,
			 "soil-to-fertilizer", \@soil_to_fertilizer_map,
			 "fertilizer-to-water", \@fertilizer_to_water_map,
			 "water-to-light", \@water_to_light_map,
			 "light-to-temperature", \@light_to_temperature_map,
			 "temperature-to-humidity", \@temperature_to_humidity_map,
			 "humidity-to-location", \@humidity_to_location_map)) {
    my ($which, $maplist) = @$pair;
    my $newlist = make_newlist($valuelist, $maplist);
#    print $which . ":\n";
#    print "valuelist: " . Dumper($valuelist);
#    print "maplist: " . Dumper($maplist);
#    print "newlist: " . Dumper($newlist);
    $valuelist = $newlist;
}

my $min_location;
foreach my $location (@$valuelist) {
    if(!defined($min_location) || $location->{'dst_first'} < $min_location) {
	$min_location = $location->{'dst_first'};
    }
}

print "min_location: $min_location\n";

#print Dumper(range_check($seeds_list[0], $seed_to_soil_map[0]));
#print Dumper(range_check($seeds_list[0], $seed_to_soil_map[1]));

sub make_newlist {
    my ($srclist, $dstlist) = @_;

    my $newlist = [];
    foreach my $orig_src (@$srclist) {
	my $unmaplist = [$orig_src];
	foreach my $dst (@$dstlist) {
	    my $newunmaplist = [];
	    foreach my $src (@$unmaplist) {
		if($src->{'dst_last'} < $dst->{'src_first'}) {
		    # src: sssssssss
		    # dst:            ddddddddddd
		    # res: uuuuuuuuu
		    push @$newunmaplist, {'dst_first' => $src->{'dst_first'},
					  'dst_last' => $src->{'dst_last'}};
		} elsif($src->{'dst_first'} > $dst->{'src_last'}) {
		    # src:              sssssssss
		    # dst: ddddddddddd
		    # res:              uuuuuuuuu
		    push @$newunmaplist, {'dst_first' => $src->{'dst_first'},
					  'dst_last' => $src->{'dst_last'}};
		} elsif($src->{'dst_first'} < $dst->{'src_first'} &&
			$src->{'dst_last'} >= $dst->{'src_first'} &&
			$src->{'dst_last'} <= $dst->{'src_last'}) {
		    # src: sssssssss
		    # dst:     ddddddddddd
		    # res: uuuummmmm
		    #
		    # src: sssssssss
		    # dst:         ddddddddddd
		    # res: uuuuuuuum
		    #
		    # src: sssssssss
		    # dst:     ddddd
		    # res: uuuummmmm
		    push @$newunmaplist, {'dst_first' => $src->{'dst_first'},
					  'dst_last' => $dst->{'src_first'} - 1};
		    push @$newlist, {'dst_first' => $dst->{'dst_first'},
				     'dst_last' => $dst->{'dst_first'} +
				     $src->{'dst_last'} - $dst->{'src_first'}};
		} elsif($src->{'dst_first'} >= $dst->{'src_first'} &&
			$src->{'dst_first'} <= $dst->{'src_last'} &&
			$src->{'dst_last'} > $dst->{'src_last'}) {
		    # src:       sssssss
		    # dst:  dddddddd
		    # res:       mmmuuuu
		    #
		    # src:       sssssss
		    # dst:  dddddd
		    # res:       muuuuuu
		    #
		    # src:       sssssss
		    # dst:       ddd
		    # res:       mmmuuuu
		    push @$newlist, {'dst_first' => $dst->{'dst_first'} +
				     $src->{'dst_first'} - $dst->{'src_first'},
				     'dst_last' => $dst->{'dst_last'}};
		    push @$newunmaplist, {'dst_first' => $dst->{'src_last'} + 1,
					  'dst_last' => $src->{'dst_last'}};
		} elsif($src->{'dst_first'} >= $dst->{'src_first'} &&
			$src->{'dst_last'} <= $dst->{'src_last'}) {
		    # src:     sssssssss
		    # dst:   ddddddddddddd
		    # res:     mmmmmmmmm
		    #
		    # src:     sssssssss
		    # dst:     ddddddddd
		    # res:     mmmmmmmmm
		    push @$newlist, {'dst_first' => $dst->{'dst_first'} +
				     $src->{'dst_first'} - $dst->{'src_first'},
				     'dst_last' => $dst->{'dst_first'} +
				     $src->{'dst_last'} - $dst->{'src_first'}};
		} elsif($src->{'dst_first'} < $dst->{'src_first'} &&
			$src->{'dst_last'} > $dst->{'src_last'}) {
		    # src:  sssssssssssss
		    # dst:      ddddddd
		    # res:  uuuummmmmmmuu
		    push @$newunmaplist, {'dst_first' => $src->{'dst_first'},
					  'dst_last' => $dst->{'src_first'} - 1};
		    push @$newlist, {'dst_first' => $dst->{'dst_first'},
				     'dst_last' => $dst->{'dst_last'}};
		    push @$newunmaplist, {'dst_first' => $dst->{'src_last'} + 1,
					  'dst_last' => $src->{'dst_last'}};
		} else {
		    print "src: " . Dumper($src);
		    print "dst: " . Dumper($dst);
		    die "Shouldn't happen!";
		}
	    }
	    $unmaplist = $newunmaplist;
	}
	foreach my $unmapped (@$unmaplist) {
	    push @$newlist, {'dst_first' => $unmapped->{'dst_first'},
			     'dst_last' => $unmapped->{'dst_last'}};
	}
    }

    return $newlist;
}
