#!/usr/bin/perl
# author, date

# library section
use strict;
use warnings FATAL => 'all';
use MCB198;

# usage statement and command line processing
die "usage: $0 <file> <k>\n" unless @ARGV == 2;
my ($file, $k) = @ARGV;

# main program
open(my $fh, $file) or die "$file not found";
my %seq = MCB198::read_multi_fasta($file);

foreach my $id (keys %seq) {
	print "$id\n";
	for (my $i = 0; $i < length($seq{$id}) -$k + 1; $i++) {
		print $i+1, " ", substr($seq{$id}, $i, $k), "\n";
	}
}

__END__

This program reads in a multi-fasta file and reports the position of each k-mer for each
sequence.