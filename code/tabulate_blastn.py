'''
For blastn searches we are going to calculate the percent coverage of the phage genome and score the longest coverage as the best hit. It doesn't matter where the hits are on the bacterial genome.

We are going to use a cutoff of 0.001 E value

'''

import sys,os,re
from phage import Phage
phage=Phage()

try:
    blastf=sys.argv[1]
except:
    sys.exit(sys.argv[0] + "< blast file>")

# read the fasta file of phages to get the lengths
lens=phage.phageSequenceLengths()
sys.stderr.write("Found " + str(len(lens)) + " sequences\n")
hits={i:{} for i in lens}



with open(blastf, 'r') as fin:
    for l in fin:
        p=l.strip().split("\t")
        e=float(p[10])
        if e > 0.001:
            continue
        m=re.findall('(NC_\d+)', p[0])
        if m == []:
            sys.stderr.write("WARNING: No phage found in " + p[0] + "\n")
            continue
        pnc = m[0]
        
        if pnc not in lens:
            sys.stderr.write("No length for " + pnc + "\n")
            continue
        
        m=re.findall('(NC_\d+)', p[1])
        if m == []:
            sys.stderr.write("WARNING: No bacteria found in " + p[1] + "\n")
            continue
        bnc = m[0]

        if bnc not in hits[pnc]:
            hits[pnc][bnc]=[]
            for i in xrange(lens[pnc]+1):
                hits[pnc][bnc].append(0)

        for i in range(int(p[6]), int(p[7])+1):
            hits[pnc][bnc][i]=1

# now print the table of phage and bacteria
bacteria=phage.completeBacteriaIDs()
phages = phage.phageIDs()

print "Bacteria\t" + "\t".join(phages)
for b in bacteria:
    print b
    for p in phages:
        if hits[p][b]:
            print "\t" + str(1.0 * sum(hits[p][b])/lens[b])
        else:
            print "\t0"
    print



        


