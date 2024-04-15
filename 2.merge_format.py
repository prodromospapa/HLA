import pandas as pd
import argparse

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--input','-i', type=str, help='input file',required=True)
parser.add_argument('--output','-o', type=str, help='output file',required=True)
args = parser.parse_args()

data = pd.read_pickle(args.input)
loci_dict = {"A":["A1","A2"],"B":["B1","B2"],"C":["C1","C2"],"DRB1":["DRB1_1","DRB1_2"],"DQB1":["DQB1_1","DQB1_2"]}

alleles_dict = {}
for locus in loci_dict:
    alleles_locus = set(sorted(data[loci_dict[locus][0]].dropna().values.tolist() + data[loci_dict[locus][1]].dropna().values.tolist()))
    alleles_dict[locus] = {}
    n = 1
    for allele in alleles_locus:
        alleles_dict[locus][allele] = n
        n += 1

final = pd.DataFrame(index = data.index)

for locus,alleles in loci_dict.items():
    final[locus] = data[loci_dict[locus]].apply(lambda x: set(sorted([alleles_dict[locus][i] for i in x if i in alleles_dict[locus]])), axis=1)
    #final[alleles[0]] = data[alleles[0]].apply(lambda x: alleles_dict[locus][x] if x in alleles_dict[locus] else 0)
    #final[alleles[1]] = data[alleles[1]].apply(lambda x: alleles_dict[locus][x] if x in alleles_dict[locus] else 0)

final.to_pickle(args.output)