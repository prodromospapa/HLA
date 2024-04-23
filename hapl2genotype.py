import pandas as pd
import glob
from numpy.random import choice
from itertools import chain


def sampling_fun_1(n_haplotype,population_size,freq):
    sampling = choice(range(n_haplotype), population_size*2,p=freq, replace=True)
    return sampling

# Load all files in "data/DKMS_10000_181022"
file_path = "data/DKMS_10000_181022"
file_list = glob.glob(file_path + "/*.xlsx")

# Iterate over each file and load it as a dataframe
final = []
population_size = 10**4
#file_list = ["data/3_loci/1977hapl_3012_2field_CBUs_3loci_excl.bl.xlsx"]
for file in file_list:
    df = pd.DataFrame(columns=["A1","A2","B1","B2","C1","C2","DRB1_1","DRB1_2","DQB1_1","DQB1_2"])
    #df = pd.DataFrame(columns=["A1","A2","B1","B2","DRB1_1","DRB1_2"])
    counter = 0
    haplotype = pd.read_excel(file).iloc[:,0].tolist()
    freq = pd.read_excel(file).iloc[:,1].tolist()
    freq = [item/sum(freq) for item in freq]
    n_haplotype = len(haplotype)

    final = [[allele.split("*")[1] for allele in item.split("~")] for item in haplotype]
    sampling = sampling_fun_1(n_haplotype,population_size,freq)
    for sample_pair in range(population_size):
        counter+=1
        row = chain(*zip(final[sampling[sample_pair*2]], final[sampling[sample_pair*2+1]]))
        df = df._append(pd.Series(row, index=df.columns), ignore_index=True)
        print(f"{counter}/{population_size}",end="\r")
    #df.to_excel("data/genotype/"+file.split("/")[-1].replace(".xlsx","")+".genotype.xlsx", index=False)
    df.to_excel("est.xlsx", index=False)
    print(f"\n{file.split("/")[-1]} is done ({file.index(file_list)+1}/{len(file_list)})")
    
