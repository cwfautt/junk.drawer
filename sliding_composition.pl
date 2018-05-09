#!/usr/bin/perl
# Chad Fautt
# 5/8/18
# inputs a fasta file and a window size; reports the GC composition in each window

# library section
use strict;
use warnings FATAL => 'all';
use lib '.';
use MCB198;



# usage statement and command line processing
die "usage: $0 <file> <Window>\n" unless @ARGV == 2;
my ($file, $window) = @ARGV;

# main part of program
my $seq = lc(MCB198::read_fasta($file));

for (my $i = 0; $i < length($seq) - $window; $i++) {
    my $sliced = substr($seq, $i, $window);
    my $GC = $sliced =~ tr/cg//;
    print($GC/$window, " ");
}
