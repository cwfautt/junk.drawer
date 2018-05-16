package MCB198;

sub read_fasta {
	my ($file) = @_;
	
	open(my $fh, $file) or die "$file not found";
	
	# read definition line, remove newline
	my $def = <$fh>;
	chomp $def;
	
	# read sequences lines, remove newline, add to $seq variable
	my $seq;
	while (my $line = <$fh>) {
		chomp $line;
		$seq .= $line;
	}
	
	return $def, $seq;
}

sub read_multi_fasta {
	my ($file) = @_;
	
	open(my $fh, $file) or die "$file not found";
	my $def;
	my %seq;
	while (my $line = <$fh>) {
		chomp $line;
		if ($line =~ /^>/) {
			$def = $line;
		} else {
			$seq{$def} .= $line;
		}
	}
	
	return %seq;
}

sub read_clustal {
	my ($file) = @_;
	
	open(my $fh, $file) or die "$file not found";
	
	# read sequences lines, remove newline, add to $seq variable
	my $seqs;
	my @array1;
	while (my $line = <$fh>) {
		chomp $line;
		my @seq = split ' ', $line;
		if (scalar(@seq) == 2){
			push(@array1, lc($seq[1]));
		}
	}
	return @array1;
}

#creates a random fasta sequence of a given length. really useless.
sub create_fasta {
	my ($seqLength) = @_;
	my $FASTA = ">RandomSeq Why would you want this\n";
	my $sequence = "";
	my @bases = qw(a c t g);
	while (length($sequence) < $seqLength){
		my $BaseIndex = int(rand(4));
		$sequence.= $bases[$BaseIndex];
		if (length($sequence) % 50 == 0 || length($sequence) == $seqLength) {
			$sequence.= "\n";
		}
	}
	$FASTA.=$sequence;

	return $FASTA;
}

# returns log base 2 of given number
sub log2 {
	my $n = shift;
	return log($n)/log(2);
}

sub entropy {
	my ($seq) = @_;
	$seq = uc($seq);

	#transliterate returns count of characters
	my $G = $seq =~ tr/G//;
	my $C = $seq =~ tr/C//;
	my $A = $seq =~ tr/A//;
	my $T = $seq =~ tr/T//;

	#calculate individiual NT frequencies
	my $G_cont = $G/length($seq);
	my $C_cont = $C/length($seq);
	my $A_cont = $A/length($seq);
	my $T_cont = $T/length($seq);

	my $H = 0;
	$H += $G_cont * MCB198::log2($G_cont) unless $G_cont == 0;
	$H += $C_cont * MCB198::log2($C_cont) unless $C_cont == 0;
	$H += $A_cont * MCB198::log2($A_cont) unless $A_cont == 0;
	$H += $T_cont * MCB198::log2($T_cont) unless $T_cont == 0;
	return ($H * -1);
}

#given hash of nucleotide frequencies at given NT position, returns array of nucleotides needed to reach threshold proportion needed for IUPAC ambigous NT code assignment. 
sub consensus_NT {
	my ($threshold, %NTcount) = @_;

	keys %NTcount; 
    my @large_keys;
    ($large_keys[0], my $large_value) = each %NTcount;
	my $total = $large_value;
    while (my ($key, $val) = each %NTcount) {
        if ($val > $large_value) {
            $large_value = $val;
			$total = $val;
            @large_keys = ($key);
        } elsif (abs($val - $large_value) < 0.00001){
            push(@large_keys, $key);
			$total += $val;
        }
    }

    foreach $NT (@large_keys){
        delete $NTcount{$NT};
    }

	#recursively add next largest NT to array until threshold is met 
	if ($total < $threshold ){
		my @temp = consensus_NT($threshold-$total, %NTcount);
		foreach $NT (@temp){
			push(@large_keys, $NT);
		}
	} 

	return @large_keys;
}

1;
