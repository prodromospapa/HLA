import pandas as pd
from multiprocessing import Pool
import numpy as np
import argparse

def process(part):
    n = part[0]
    part = part[1]
    df = pd.DataFrame(columns=loci,index=id)
    if args.nine:
        df['DQB1_9/10'] = ""
    df = df.apply(lambda x: x.apply(lambda _: []))
    for row_index in part:
        row = data_np[row_index][1:]
        row_name = id[row_index]
        for row_total in data_np:
            counter = 0
            row_total_name = id[row_total[0]]
            row_total = row_total[1:]
            for locus in loci:
                locus_index = loci_index[locus]
                genotype = row[locus_index]             
                if row_total_name == row_name:
                    continue
                elif not genotype:
                   continue
                if (genotype[0] in row_total[locus_index]) and (genotype[1] in row_total[locus_index]): #(normal == row_total[locus]) or (reversed == row_total[locus]): # If the locus is heterozygous
                    counter+=1
                    df.at[row_name,locus].append(row_total_name)
                elif genotype[0] == genotype[1] and genotype[0] in row_total[locus_index]: # If the locus is homozygous
                    counter+=1
                    df.at[row_name,locus].append(row_total_name)
        if n==1:
            print(f"{row_index+1}/{len(part)}",end="\r")
    return df

def run(n):  # Number of equal parts
    partitions = list(zip(range(1,n+1),np.array_split(range(len(data_np)), n)))
    p = Pool(processes=n)
    data = p.map(process, partitions)
    p.close()
    return pd.concat(data)

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--threads','-t', type=int, help='Number of threads to use')
parser.add_argument('--input','-i', type=str, help='Input file') #data/Greek_BMDs_2fields/70077gen_78716BMDs_2fields_5loci_excl.bl.xlsx
parser.add_argument('--loci','-l', type=str, help='Loci to include')
parser.add_argument('--nine','-n', action='store_true', help='DQB1 9/10')

args = parser.parse_args()

if "," not in args.loci:
    loci = [args.loci]  # loci are passed as command line arguments, ["A","B", "C", "DRB1", "DQB1", "DPB1"]
else:
    loci = args.loci.split(",")
    loci = [i.strip() or i for i in loci]

if len(loci) != 5 and args.nine:
    print("DQB1 9/10 can only be used with 5 loci")
    exit()

data = pd.read_pickle("all.pickle")
id = data["ID"].tolist()
data = data.drop(columns=["ID"])
data[["A","B","C","DRB1","DQB1"]] = data[["A","B","C","DRB1","DQB1"]].map(eval)
data_np = data.to_numpy()
loci_index = {"A":0,"B":1,"C":2,"DRB1":3,"DQB1":4}

run(args.threads).to_pickle("output_np_merge.pickle")#.to_csv("output_np_merge_t.csv")
#python3 hom_all_par_np_merge.py -t 25 -i all_np.csv -l "A,B,C,DRB1,DQB1" -n