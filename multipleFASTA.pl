#!/usr/bin/perl
# Chad Fautt, 5/7/18

# library section
use strict;
use warnings FATAL => 'all';
use lib '.';
use MCB198;

# usage statement and command line processing
die "usage: $0 <seqNum> <seqMin> <seqMax>\n" unless @ARGV == 3;
my ($seqNum, $seqMin, $seqMax) = @ARGV;

# main part of program
my $outString = "";
for (my $i = 0; $i < $seqNum; $i++){
	my $len = int($seqMin + rand($seqMax-$seqMin));
	$outString.= MCB198::create_fasta($len);
}
print($outString);
