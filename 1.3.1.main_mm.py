from multiprocessing import Pool
import numpy as np
import argparse
import pandas as pd
import os

def mismatch(donor,recepient):
    if not donor or not recepient:
        return -1 # Missing data
    if args.direction == "GvH":
        return len(donor - recepient)
    elif args.direction == "HvG":
        return len(recepient - donor)

def process(part):
    n = part[0]
    part = list(part[1])
    if part:
        arr = np.ones((len(part), len(data_np), len(loci_index_list)), dtype=np.int8)
        counter = 0
        for i, row_index in enumerate(part):
            row = data_np[row_index]
            for j, itter_row in enumerate(data_np):
                arr_row = np.empty(len(loci_index_list), dtype=np.int8)
                counter += 1
                for locus in loci_index_list:
                    genotype_donor = row[locus]
                    if row_index != j:
                        genotype_recepient = itter_row[locus]
                        arr_row[locus] = mismatch(genotype_donor, genotype_recepient)
                    else:
                        arr_row[locus] = -1
                arr[i,j] = arr_row
                if n == 0:
                    print(f"{i+1}/{len(part)}", end="\r")
        return arr

def run(n):  # Number of equal parts
    partitions = list(zip(range(n),np.array_split(data.index, n)))
    p = Pool(processes=n)
    return_data = p.map(process, partitions)
    p.close()
    return np.concatenate(return_data,axis=0)

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--threads','-t', type=int, help='Number of threads to use', required=True)
parser.add_argument('--input','-i',default="all.pickle", type=str, help='Input file')
parser.add_argument('--direction','-d', choices=['GvH','HvG'], help='Direction(GvH or HvG)', required=True)

args = parser.parse_args()

loci = ["A","B","C","DRB1","DQB1"]

data = pd.read_pickle(args.input)
data_np = data[loci].to_numpy()

loci_index = {"A":0,"B":1,"C":2,"DRB1":3,"DQB1":4}
loci_index_list = [loci_index[locus] for locus in loci]

threads = args.threads
if threads > os.cpu_count():
    threads = int(round(os.cpu_count()*0.8,0))
final = run(threads)
with open(f'all_{args.direction}.npy', 'wb') as f:
    np.save(f,final)

#python3 1.3.1.main_mm.py -t 25 -d HvG