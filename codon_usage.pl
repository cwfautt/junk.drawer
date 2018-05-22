#!/usr/bin/perl
# Chad Fautt

#USE: Write a program that reads in a multi-fasta file and
# reports the codon usage of the various transcripts.

# library section
use strict;
use warnings FATAL => 'all';
use lib '.';
use MCB198;
use Data::Dumper;


# usage statement and command line processing
die "usage: $0 <file>\n" unless @ARGV == 1;
my ($file) = @ARGV;

# main part of program

my %cDNA = MCB198::read_multi_fasta($file);

my %codon_use;

while ((my $k, my $v) = each %cDNA){
	for (my $i = 0; $i < length($v) - 2; $i += 3) {
		$codon_use{$k}{substr($v, $i, 3)}++
	}
}

foreach my $transcript (sort keys %codon_use) {
    foreach my $codon (keys %{ $codon_use{$transcript} }) {
        print "$transcript, $codon: $codon_use{$transcript}{$codon}\n";
    }
}




