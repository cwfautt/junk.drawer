#!/usr/bin/perl
# Chad Fautt
# 5/8/18
# inputs a fasta file, a window size, sequence replacement preference(N="N", n=lowercase), and H threshold; 
# returns a sequence with all windows below threshold modified in preferred manner.

# library section
use strict;
use warnings FATAL => 'all';
use lib '.';
use MCB198;



# usage statement and command line processing
die "usage: $0 <file> <Window> <N/n> <MinH>\n" unless @ARGV == 4 && lc($ARGV[2]) eq "n";
my ($file, $window, $Nn, $MinH) = @ARGV;

# main part of program
my %seqs = MCB198::read_multi_fasta($file);
my $outSeqs;

keys %seqs; 
while (my($k, $v) = each %seqs) {
    my $seq = uc($v);
    my $outSeq = $seq;
    
    for (my $i = 0; $i <= length($seq) - $window; $i++) {
        my $sliced = substr($seq, $i, $window);
        my $H = MCB198::entropy($sliced);

        if ($H < $MinH) {
            if ($Nn eq "N") {substr($outSeq, $i, $window) =~ tr/GACT/NNNN/} 
            elsif ($Nn eq "n") {substr($outSeq, $i, $window) =~ tr/GACT/gact/}
        } 
    }
    $outSeqs .= $k;
    $outSeqs .= "\n";
    $outSeqs .= $outSeq;
    $outSeqs .= "\n";
}

print($outSeqs);
