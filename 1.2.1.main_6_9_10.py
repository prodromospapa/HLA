from multiprocessing import Pool
import numpy as np
import argparse
import pandas as pd
import os

def process(part):
    n = part[0]
    part = list(part[1])
    if part:
        df = pd.DataFrame(columns=["6/6","9/10","10/10"],index=id[part[0]:part[-1]+1])
        df = df.apply(lambda x: x.apply(lambda _: []))
        counter = 0
        for i, row_index in enumerate(part):
            row = data_np[row_index]
            for j, itter_row in enumerate(data_np):
                counter += 1
                if row_index != j:
                    row_loci = loci_list[row_index]
                    if row_loci == 3 and (row[[0,1,3]]==itter_row[[0,1,3]]).all():
                        df.at[id[row_index],"6/6"].append(id[j])
                    elif row_loci == 5:
                        if (row[:4]==itter_row[:4]).all():
                            if (row[4]==itter_row[4]):
                                df.at[id[row_index],"10/10"].append(id[j])
                            elif len(row[4]-itter_row[4]) == 1:
                                df.at[id[row_index],"9/10"].append(id[j])
                if n == 0:
                    print(f"{i+1}/{len(part)}", end="\r") 
        return df

def run(n):  # Number of equal parts
    partitions = list(zip(range(n),np.array_split(data.index, n)))
    p = Pool(processes=n)
    return_data = p.map(process, partitions)
    p.close()
    return pd.concat(return_data)

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--threads','-t', type=int, help='Number of threads to use', required=True)
parser.add_argument('--input','-i',default="all.pickle", type=str, help='Input file')

args = parser.parse_args()

loci = ["A","B","C","DRB1","DQB1"]

data = pd.read_pickle(args.input)
loci_list = data["loci"].tolist()
id = data["ID"].tolist()
data_np = data[loci].to_numpy()
loci_index = {"A":0,"B":1,"C":2,"DRB1":3,"DQB1":4}
loci_index_list = [loci_index[locus] for locus in loci]

threads = args.threads
if threads > os.cpu_count():
    threads = int(round(os.cpu_count()*0.8,0))
final = run(threads)
#final = final[~final.apply(lambda row: all(x == [] for x in row), axis=1)]
final.to_pickle("final_6_9_10.pickle")

#python3 2.main_6_9_10.py -t 25

#a['10/10'].sort_values(key=lambda col: col.str.len())