#!/usr/bin/perl  
# poisson.pl by Chad
use strict; use warnings;  

# lambda : (int > 0) is expected coverage. if 10X coverage, lambda = 10. 
# K: (int >= 0) is number of observations seen (actual coverage)
my ($lambda, $k) = @ARGV;  

while ( $lambda !~ /^\d+$/ || $lambda < 1) {
    print "Oh, man, I'm really sorry, but something went wrong. Try entering a value for lambda that is an integer greater than 0: ";
    $lambda = <STDIN>
}
while ( $k !~ /^\d+$/) {
    print "Oh, man, I'm really sorry, but something went wrong. Try entering a value for K that is an integer greater than or equal to 0: ";
    $k = <STDIN>
}

#naive factorial calculation
my $count = $k;
my $fact_k = 1;
while($count > 0) {$fact_k *= $count; $count--}

my $prob = ((2.71828 ** (-$lambda))*($lambda**$k))/($fact_k);

print "$prob\n";
