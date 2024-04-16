import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse
from collections import Counter


with open('all_original.pickle', 'rb') as f:
        data = np.load(f,allow_pickle=True)
big_dic={}
for loci in ["A","B","C","DRB1","DQB1"]:
        loci_list=data[loci].tolist()         
        loci_dict = Counter([j for i in loci_list for j in i ])
        loci_dict = {k:v/len(loci_list) for k,v in loci_dict.items()}
        big_dic[loci]=loci_dict
print(big_dic)
