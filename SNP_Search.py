"""This finds which SNPs are in which sequences, given coordinates for the SNPs and the start/end of the sequences"""

import random
from decimal import getcontext, Decimal

#fill both SNP database and exons with random (chr,coord),(chr,coord,coord) entries, respectively.... FOR TESTING PURPOSES ONLY
SNPs = []
exons = []
while len(SNPs) < 600_000:
    SNPs.append((random.randint(1,24), random.randint(1,1.5e8))) 
while len(exons) < 20_000: 
    coord1 = random.randint(1,(1.5e8-15_000))
    coord2 = coord1 + random.randint(4000,15_000)
    exons.append((random.randint(1,24), coord1, coord2))

""" SORTING AND INDEXING DATA """

chr = {}
#seperate SNPs by chr
for i in SNPs:
    if i[0] in chr:
        chr[i[0]].append(i[1])
    else:
        chr[i[0]] = [i[1]]

#seperate exons by chr and index them
e = len(str(len(exons)))
getcontext().prec = 18
indexing = 1/10**e #the indexing of exons is done by turning them into floats. the digits after the decimal point are the index and allow easy discrimination between them and the SNPs later.
for i in exons:
    if i[0] in chr:
        StartIndexed = Decimal(i[1] + indexing).quantize(Decimal(str(1+(1/10**e))))
        chr[i[0]].append(StartIndexed)
        EndIndexed = Decimal(i[2] + indexing).quantize(Decimal(str(1+(1/10**e))))
        chr[i[0]].append(EndIndexed)
    else:
        chr[i[0]] = [i[1] + indexing, i[2] + indexing]
    indexing += 1/10**e

#sort SNP and exon coordinates in each chromosome
for i in chr:
    chr[i].sort()

""" SEARCH """

staging = {} #temporary staging area for associating SNPs with exons
matches = {} #holds the exons as keys, and each SNP within it in a list
for i in chr:
    #moves through the sorted array of each chr, associating SNPs and exons
    for j in chr[i]:
        #the only things in the array that arent ints are the start/end of exons, indexed as float values (xxxx.04-xxxxx.04 is exon #4)
        if type(j) is not int:
            exonIndex = int(str(j).split(".")[1])
            #if we found the end of a particular exon in chr, move it from staging to matches
            if exons[exonIndex-1] in staging:
                matches[exons[exonIndex-1]] = staging[exons[exonIndex-1]]
                staging.pop(exons[exonIndex-1])
            #if the exon is not already in staging, we must be at its start point; add it to staging
            else:
                staging[exons[exonIndex-1]] = []
        #associate ints with all exons currently in staging
        else:
            for exon in staging:
                staging[exon].append(j)

for i in matches:
    print(f"sequence {i}: {len(matches[i])} SNPs {matches[i]}")
