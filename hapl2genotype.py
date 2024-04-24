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

final = []
population_size = 10**4
for file in file_list:
    df = pd.DataFrame(columns=["A1","A2","B1","B2","C1","C2","DQB1_1","DQB1_2","DRB1_1","DRB1_2"])
    counter = 0
    haplotype = pd.read_excel(file).iloc[:,0].tolist()
    
    freq = pd.read_excel(file).iloc[:,1].tolist()
    freq = [item/sum(freq) for item in freq]

    final = [[allele.split("*")[1] for allele in item.split("~")] for item in haplotype]
    sampling = sampling_fun_1(len(haplotype),population_size,freq)

    for sample_pair in range(population_size):
        counter+=1
        row = chain(*zip(final[sampling[sample_pair*2]], final[sampling[sample_pair*2+1]]))
        df = df._append(pd.Series(row, index=df.columns), ignore_index=True)
        print(f"{counter}/{population_size}",end="\r")
    df = df[["A1","A2","B1","B2","C1","C2","DRB1_1","DRB1_2","DQB1_1","DQB1_2"]]
    df.to_excel("data/genotype/"+file.split("/")[-1].replace(".xlsx","")+".genotype.xlsx", index=False)
    print(f"\n{file.split("/")[-1]} is done ({file_list.index(file)+1}/{len(file_list)})")