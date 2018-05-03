#!/usr/bin/env python

ofile = 'references/OM-RGC.gff'
fna_file = 'references/OM-RGC.fna'
map_file = 'references/OM-RGC.functional.map'

length = {}
active = None
for line in open(fna_file):
    if line[0] == '>':
        active = line[1:].strip().split()[0]
    else:
        length[active] = str(len(line))

with open(ofile, 'wt') as output:
    for i,line in enumerate(open(map_file)):
        tokens = line.rstrip('\n').split('\t')
        if i == 0:
            headers = tokens
            ix = headers.index('eggNOG_OG')
            continue
        f = 'eggnog45'
        gene = tokens[0]
        output.write("\t".join([
                gene,
                "mocat",
                f,
                "1",
                length[gene],
                ".",
                ".",
                ".",
                "NOG={}".format(tokens[ix])]))
        output.write("\n")
