#!/usr/bin/perl
# Chad Fautt, 5/7/18

# library section
use strict;
use warnings FATAL => 'all';
use lib '.';
use MCB198;

# usage statement and command line processing
die "usage: $0 <seqLen> \n" unless @ARGV == 1;
my ($seqLen) = @ARGV;

# main part of program
print MCB198::create_fasta($seqLen);
