#!/usr/bin/perl
# Chad Fautt

#USE: takes one clustalW formatted multiple DNA sequence alignment, outputs basic consensus sequence.

# library section
use strict;
use warnings FATAL => 'all';
use lib '.';
use MCB198;



# usage statement and command line processing
die "usage: $0 <file>\n" unless @ARGV == 1;
my ($file) = @ARGV;

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
    #find consensus NT at position $i
    keys %NTcount; 
    my $percent;
    my @large_keys;
    ($large_keys[0], my $large_value) = each %NTcount;

    while (my ($key, $val) = each %NTcount) {
        if ($val > $large_value) {
            $large_value = $val;
            @large_keys = ($key);
        } elsif ($val == $large_value){
            push(@large_keys, $key);
        }
    }
    foreach my $NT (@large_keys){
        delete $NTcount{$NT};
    }



    $consensus .= $large_keys[0];
}
print($consensus, "\n");

