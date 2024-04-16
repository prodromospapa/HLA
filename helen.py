import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse
from collections import Counter


def counter_genotype(data):
        big_dic={}
        for loci in ["A","B","C","DRB1","DQB1"]:
                loci_list=data[loci].tolist()         
                loci_dict = Counter([j for i in loci_list for j in i ])
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
                        for allele in genotypes[base].loc[i]:
                                if allele not in final[base]:
                                        final[base][allele] = {0:(mm[i]==0).sum(),1:(mm[i]==1).sum(),2:(mm[i]==2).sum()}
                                else:
                                        for j in range(3):
                                                final[base][allele][j] += (mm[i]==j).sum()
                                print(f"{counter}/{len(data[base].index)*5*2}",end="\r")
        for base in ["A","B","C","DRB1","DQB1"]:
                counter+=1
                for allele in final[base]:
                        total = sum(final[base][allele].values())
                        for k in final[base][allele]:
                                final[base][allele][k] = final[base][allele][k]/total
                        print(f"{counter}/{len(data[base].index)*5*2}",end="\r")
        return final

with open('all_original.pickle', 'rb') as f:
        genotypes = np.load(f,allow_pickle=True)

with open('all_HvG.npy', 'rb') as f:
        mm = np.load(f,allow_pickle=True)

big_dic = counter_genotype(genotypes)

source = genotypes[genotypes['source']=='CBU']
final = counter_allele(source)

df = pd.DataFrame(final)
pd.DataFrame(big_dic).reindex(df.index)

