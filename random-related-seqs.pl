#!/usr/bin/perl
# Chad Fautt, 5/7/18

# library section
use strict;
use warnings FATAL => 'all';
use lib '.';
use MCB198;

# usage statement and command line processing
die "usage: $0 <seqLen> \n" unless @ARGV == 1;
my ($seqLength) = @ARGV;

# main part of program

my $FASTA = ">RandomSeq\n";
my $sequence = "";
my @bases = qw(a c t g);
while (length($sequence) < $seqLength){
    my $BaseIndex = int(rand(4));
    $sequence.= $bases[$BaseIndex];
    if (length($sequence) == $seqLength) {
        $sequence.= "\n";
    }
}
$FASTA.=$sequence;

for (my $i = 0; $i < 25; $i++){
    my $title = ">Randomseq-$i";
    my $relatedSeq = "";
    for (my $j = 0; $j < length($sequence); $j++){
        if (rand() < 0.12){
            my $BaseIndex = int(rand(4));
            $relatedSeq .= $bases[$BaseIndex];
        } else {
            $relatedSeq .= substr($sequence, $j-1, 1);
        }
        #random indels
        if (rand() < 0.03) {
            my $BaseIndex = int(rand(4));
            $relatedSeq .= $bases[$BaseIndex];
        } elsif (rand() > 0.97) {
            $j++
        }
    }
    $relatedSeq.= "\n";
    $FASTA .= $title;
    $FASTA .= $relatedSeq;
}
print($FASTA);