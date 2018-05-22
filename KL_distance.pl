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

# pseudo:

# modify above loop to tally up ALL codons, and also store the count for each codon in a new has table.
# divide to get probability of each message in genome.
# do the same thing for each. fucking. gene. and use the following formula to calculate distance of each gene to whole genome:
# ---- (need to add one to everything to compensate for inevitable zeros in individual genes.)
# Distance = SUM of (probability of given codon in genome) * log_2(probability in genome/probability in gene)
#
# just store all distances for each gene, maybe report anything greater than two S.D. from mean distance?


