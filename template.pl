#!/usr/bin/perl
# author, date

# library section
use strict;
#use warnings FATAL => 'all';
use MCB198;
use POSIX;

# usage statement and command line processing
die "usage: $0 <seqLength>\n" unless @ARGV == 1;
my ($seqLength) = @ARGV;

# main part of program
my $FASTA = ">RandomSeq Why would you want this\n";
my $sequence = "";
my @bases = qw(a c t g);
while (length($sequence) < $seqLength){
	my $BaseIndex = floor(rand(4));
	#print $bases[0];
	$sequence.= $bases[$BaseIndex];
	if (length($sequence) % 50 == 0){
		$sequence.= "\n";
	}
}
$FASTA.=$sequence;
print($FASTA);
