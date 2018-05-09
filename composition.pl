#!/usr/bin/perl
# Chad Fautt
# 5/8/18
# inputs a fasta file and reports the GC composition, nucleotide frequency, and entropy of the sequence. 

# library section
use strict;
use warnings FATAL => 'all';
use lib '.';
use MCB198;



# usage statement and command line processing
die "usage: $0 <file>\n" unless @ARGV == 1;
my ($file) = @ARGV;

# main part of program

my $seq = lc(MCB198::read_fasta($file));

#transliterate returns count of characters
my $G = $seq =~ tr/g//;
my $C = $seq =~ tr/c//;
my $A = $seq =~ tr/a//;
my $T = $seq =~ tr/t//;

#calculate individiual NT frequencies
my $G_cont = $G/length($seq);
my $C_cont = $C/length($seq);
my $A_cont = $A/length($seq);
my $T_cont = $T/length($seq);

#GC content
my $GC_cont = $G_cont + $C_cont;

#entropy of sequence
my $H = 0;
$H += $G_cont * MCB198::log2($G_cont) unless $G_cont == 0;
$H += $C_cont * MCB198::log2($C_cont) unless $C_cont == 0;
$H += $A_cont * MCB198::log2($A_cont) unless $A_cont == 0;
$H += $T_cont * MCB198::log2($T_cont) unless $T_cont == 0;
$H *= -1;

printf("G: %.3f\nC: %.3f\nA: %.3f\nT: %.3f\nGC: %.3f\nH: %.3f\n", $G_cont, $C_cont, $A_cont, $T_cont, $GC_cont, $H);
