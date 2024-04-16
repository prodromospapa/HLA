import numpy as np
import pandas as pd
import argparse
from collections import Counter

def percentage(choose,direction):
    f = open(f'all_{direction}.npy', 'rb')
    all = pd.read_pickle("all.pickle")
    all = all[all['source'].isin(choose)].reset_index(drop=True)
    data = np.load(f)[all.index,:,:]
    arr = np.empty((len(data),3), dtype=list)
    for i,sample in enumerate(data):
        #1 loci
        full = []
        for j in range(5):
            if j in [2,4] and all['loci'][i] == 3:
                full.append(None)
            else:
                row = sample[:,j]
                length = len(row)  - (row==-1).sum()
                count  = {0:(row ==0).sum()*100/length,1:(row==1).sum()*100/length,2:(row ==2).sum()*100/length}
                full.append(count)

        arr[i,0] = full

        #3 loci
        row = np.concatenate(sample[:,[0,1,3]])
        length = len(row)  - (row==-1).sum()
        count_3  = {0:(row ==0).sum()*100/length,1:(row==1).sum()*100/length,2:(row ==2).sum()*100/length}
        arr[i,1] = count_3
        
        #5 loci
        if all['loci'][i] == 5:
            row = np.concatenate(sample)
            length = len(row) - (row==-1).sum()
            count_5  = {0:(row ==0).sum()*100/length,1:(row==1).sum()*100/length,2:(row ==2).sum()*100/length}
            arr[i,2] = count_5
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

with open(f'{args.choose}.npy', 'wb') as f:
    np.save(f,percentage(choose,args.direction))