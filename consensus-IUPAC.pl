#!/usr/bin/perl
# Chad Fautt

#USE: takes one clustalW formatted multiple DNA sequence alignment, outputs basic $consensus sequence.

# library section
use strict;
use warnings FATAL => 'all';
use lib '.';
use MCB198;
use experimental 'smartmatch';



# usage statement and command line processing
die "usage: $0 <file> <threshold>\n" unless @ARGV == 2;
my ($file, $threshold) = @ARGV; #threshold between 0-1.

# main part of program

my @aligned = MCB198::read_clustal($file);

my $consensus;
for (my $i = 0; $i < length($aligned[0]); $i++){

    #tally the presence of each nucleotide at position $i
    my %NTcount = ( a => 0, c => 0, g => 0, t => 0, '-' => 0 );
    for (my $j = 0; $j < scalar(@aligned); $j++){
        $NTcount{substr($aligned[$j], $i, 1)}++
    }

    #convert to frequencies
    keys %NTcount; 
    foreach my $freq (keys %NTcount){
        $NTcount{$freq} /= scalar(@aligned);
    }

    #if you can get to threshold without gaps, find $consensus NTs at position $i
    my @nucs = ();
    if ($NTcount{'-'} < (1-$threshold)){
        delete $NTcount{'-'};
        @nucs = MCB198::consensus_NT($threshold, %NTcount);
    }

    #assign ambiguity codes
    if (scalar(@nucs) == 1) { $consensus .= uc($nucs[0]) }
    elsif (scalar(@nucs) == 2){
        if ('c' ~~ @nucs && 't' ~~ @nucs) { $consensus .= 'Y' } 
        elsif ('a' ~~ @nucs && 'g' ~~ @nucs) { $consensus .= 'R' } 
        elsif ('a' ~~ @nucs && 't' ~~ @nucs) { $consensus .= 'W' } 
        elsif ('c' ~~ @nucs && 'g' ~~ @nucs) { $consensus .= 'S' } 
        elsif ('t' ~~ @nucs && 'g' ~~ @nucs) { $consensus .= 'K' } 
        elsif ('a' ~~ @nucs && 'c' ~~ @nucs) { $consensus .= 'M' } 
    }
    elsif (scalar(@nucs) == 3) {
        if (!('c' ~~ @nucs)) { $consensus .= 'D' } 
        if (!('t' ~~ @nucs)) { $consensus .= 'V' }
        if (!('g' ~~ @nucs)) { $consensus .= 'H' }
        if (!('a' ~~ @nucs)) { $consensus .= 'B' }
    }
    elsif (scalar(@nucs) == 4) { $consensus .= "N" }
}
print($consensus);