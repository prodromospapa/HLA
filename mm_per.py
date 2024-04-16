import numpy as np
import pandas as pd
import argparse
from collections import Counter

def percentage(choose,direction):
    f = open(f'all_{direction}.npy', 'rb')
    all = pd.read_pickle("all.pickle")
    data = np.load(f)[all[all['source'].isin(choose)].index,:,:]
    arr = np.empty((len(data),3), dtype=list)
    for i,sample in enumerate(data):
        #1 loci
        full = []
        for j in range(5):
            if not sample[:,j].all() == -1:
                count = dict(sorted(Counter(sample[:,j]).items()))
                count.pop(-1)
                total_count = sum(count.values())
                percentages = {key: value/total_count * 100 for key, value in count.items()}
                full.append(percentages)
            else:
                full.append([None])
        arr[i,0] = full

        #3 loci
        count_3 = dict(sorted(Counter(np.concatenate(sample[:,[0,1,3]]).tolist()).items()))
        count_3.pop(-1)
        total_count_3 = sum(count_3.values())
        percentages_3 = {key: value/total_count_3 * 100 for key, value in count_3.items()}
        arr[i,1] = percentages_3
        
        #5 loci
        if not sample[:,4].all() == -1:
            count_5 = dict(sorted(Counter(np.concatenate(sample).tolist()).items()))
            count_5.pop(-1)
            total_count_5 = sum(count_5.values())
            percentages_5 = {key: value/total_count_5 * 100 for key, value in count_5.items()}
            arr[i,2] = percentages_5
        print(f"{i+1}/{len(data)}", end="\r")
    return arr

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')


parser.add_argument('--direction','-d', choices=['GvH','HvG'], help='Direction(GvH or HvG)', required=True)
parser.add_argument('--choose','-c', choices=['BMD','CBU','all'],type=str, help='Direction(GvH or HvG)', required=True)

args = parser.parse_args()

if args.choose == 'all':
    choose = ['BMD','CBU']
else:
    choose = [args.choose]

with open(f'duno.npy', 'wb') as f:
    np.save(f,percentage(choose,args.direction))