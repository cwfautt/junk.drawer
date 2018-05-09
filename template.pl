#!/usr/bin/perl
# Chad Fautt

# library section
use strict;
use warnings FATAL => 'all';
use MCB198;


# usage statement and command line processing
die "usage: $0 <seqLength>\n" unless @ARGV == 1;
my ($seqLength) = @ARGV;

# main part of program
