import numpy as np
import pandas as pd
import argparse
from collections import Counter


def counter_genotype(data):
        big_dic={}
        for loci in ["A","B","C","DRB1","DQB1"]:
                loci_list=[j for i in data[loci].tolist() for j in i]
                loci_dict = Counter(loci_list)
                loci_dict = {k:v/len(loci_list) for k,v in loci_dict.items()}
                big_dic[loci]=loci_dict
        return big_dic

def counter_allele(data):
        final = {}
        counter = 0
        for base in ["A","B","C","DRB1","DQB1"]:
                final[base] = {}
                for i in data[base].index:
                        counter+=1
                        if args.type == "allele":
                                for allele in genotypes[base].loc[i]:
                                        if allele not in final[base]:
                                                final[base][allele] = {0:(mm[i]==0).sum(),1:(mm[i]==1).sum(),2:(mm[i]==2).sum()}
                                        else:
                                                for j in range(3):
                                                        final[base][allele][j] += (mm[i]==j).sum()
                        else:
                                allele = "_".join(genotypes[base].loc[i])
                                if allele not in final[base]:
                                        final[base][allele] = {0:(mm[i]==0).sum(),1:(mm[i]==1).sum(),2:(mm[i]==2).sum()}
                                else:
                                        for j in range(3):
                                                final[base][allele][j] += (mm[i]==j).sum()
                        print(f"{counter}/{len(data[base].index)*5}",end="\r")
        for base in ["A","B","C","DRB1","DQB1"]:
                for allele in final[base]:
                        total = sum(final[base][allele].values())
                        for k in final[base][allele]:
                                final[base][allele][k] = final[base][allele][k]/total
        return final

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--choose','-c', choices=['BMD','CBU','all'],type=str, help='Direction(GvH or HvG)', required=True)
parser.add_argument('--direction','-d', choices=['GvH','HvG'], help='Direction(GvH or HvG)', required=True)
parser.add_argument('--type','-t', choices=['allele','genotype'], help='Type of data to be saved', required=True)

args = parser.parse_args()

with open('all_original.pickle', 'rb') as f:
        genotypes = np.load(f,allow_pickle=True)

with open(f'all_{args.direction}.npy', 'rb') as f:
        mm = np.load(f,allow_pickle=True)

if args.choose in ['BMD','CBU']:
        type = genotypes[genotypes['type']==args.choose]
else:
        type = genotypes

mm_per = counter_allele(type)
al_per = counter_genotype(genotypes)

mm_per_df = pd.DataFrame(mm_per)
al_per_df = pd.DataFrame(al_per).reindex(mm_per_df.index)

mm_per_df.to_pickle(f"{args.choose}_{args.direction}_{args.type}_mm_per.pickle")
al_per_df.to_pickle(f"{args.choose}_{args.direction}_{args.type}_freq_per.pickle")

#python3 helen.py -c CBU -d HvG