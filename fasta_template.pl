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
my ($def, $seq) = MCB198::read_fasta($file);

for (my $i = 0; $i < length($seq) -$k + 1; $i++) {
	print $i+1, " ", substr($seq, $i, $k), "\n";
}

__END__

This program reads in a fasta file and reports the position of each k-mer. The file must
have just one sequence in it.