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

1;
