import random
from decimal import getcontext, Decimal

"""This finds which of (queries) are at least partially in each of (seqs),
given start & end coordinates of the sequences and queries."""

#fill both query database and seqs with random (chr,coord,coord) entries.... FOR TESTING PURPOSES ONLY
queries = []
seqs = []
while len(queries) < 600_000:
    coord1 = random.randint(1,1.5e8-500)
    coord2 = coord1 + random.randint(0,500)
    queries.append((random.randint(1,24), coord1, coord2)) 
while len(seqs) < 20_000: 
    coord1 = random.randint(1,(1.5e8-15_000))
    coord2 = coord1 + random.randint(4000,15_000)
    seqs.append((random.randint(1,24), coord1, coord2))

""" SORTING AND INDEXING DATA """

chr = {}
queryHash = {}
#seperate queries by chr and add each coordinate as a key to the hash table 'queryHash' with their index in 'queries' as the value
for i in range(len(queries)):
    queryHash[queries[i][1]] = i
    queryHash[queries[i][2]] = i
    if queries[i][0] in chr:
        chr[queries[i][0]].append(queries[i][1])
        chr[queries[i][0]].append(queries[i][2])
    else:
        chr[queries[i][0]] = [queries[i][1], queries[i][2]]
#seperate seqs by chr and index them
e = len(str(len(seqs)))
getcontext().prec = 18
indexing = 1/10**e #the indexing of seqs is done by turning them into floats. the digits after the decimal point are the index and allow easy discrimination between them and the queries later.
for i in seqs:
    if i[0] in chr:
        StartIndexed = Decimal(i[1] + indexing).quantize(Decimal(str(1+(1/10**e))))
        chr[i[0]].append(StartIndexed)
        EndIndexed = Decimal(i[2] + indexing).quantize(Decimal(str(1+(1/10**e))))
        chr[i[0]].append(EndIndexed)
    else:
        chr[i[0]] = [i[1] + indexing, i[2] + indexing]
    indexing += 1/10**e

#sort query and seq coordinates in each chromosome
for i in chr:
    chr[i].sort()

""" SEARCH """

staging = {} #temporary staging area for associating queries with seqs
matches = {} #holds the seqs as keys, and each query within it in a list
for i in chr:
    #moves through the sorted array of each chr, associating queries and seqs
    for j in chr[i]:
        #the only things in the array that arent ints are the start/end of seqs, indexed as float values (xxxx.04-xxxxx.04 is seq #4)
        if type(j) is not int:
            exonIndex = int(str(j).split(".")[1])
            #if we found the end of a particular seq in chr, move it from staging to matches
            if seqs[exonIndex-1] in staging:
                matches[seqs[exonIndex-1]] = staging[seqs[exonIndex-1]]
                staging.pop(seqs[exonIndex-1])
            #if the seq is not already in staging, we must be at its start point; add it to staging
            else:
                staging[seqs[exonIndex-1]] = []
        #associate ints with all seqs currently in staging
        else:
            for seq in staging:
                #only add if I haven't already associated it
                if queries[queryHash[j]] not in staging[seq]:
                    staging[seq].append(queries[queryHash[j]])
                    
for i in matches:
    print(f"sequence {i}: {len(matches[i])} hit(s) -> {matches[i]}")
