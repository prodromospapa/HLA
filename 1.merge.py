import pandas as pd
import numpy as np
from multiprocessing import Pool
import argparse

def merge1(part):
    n = part[0]
    part = list(part[1])
    if part:
        final = pd.DataFrame()
        counter = 0
        final_dict = {"ID":[],"type":[],"loci":[],"generation":[],"A1":[],"A2":[],"B1":[],"B2":[],"C1":[],"C2":[],"DRB1_1":[],"DRB1_2":[],"DQB1_1":[],"DQB1_2":[]}
        for index,row in data.iloc[part].iterrows():
            counter+=1
            loci_3 = ['A1', 'A2', 'B1', 'B2', 'DRB1_1', 'DRB1_2']
            loci_5 = ['C1', 'C2', 'DQB1_1', 'DQB1_2']
            if all(row[loci_3].notna()):
                if any(row[loci_5].isna()):
                    final_dict["loci"].append(3)
                    for locus in loci_3+loci_5:
                        try:
                            value = ":".join(row[locus].split(":")[:2])
                            final_dict[locus].append(value)
                        except Exception:
                            final_dict[locus].append(np.nan)
                elif all(row[loci_5].notna()):
                    final_dict["loci"].append(5)
                    for locus in loci_3+loci_5:
                        value = ":".join(row[locus].split(":")[:2])
                        final_dict[locus].append(value)
                else:
                    continue

                final_dict["ID"].append(row["ID"])
                final_dict["generation"].append(row["GENERATION"])
                if row['TYPE'] == 'MD':
                    final_dict["type"].append('BMD')
                else:
                    final_dict["type"].append('CBU')
                    
            if n == 0:
                print(f"{counter}/{len(part)}",end="\r")
        return pd.DataFrame(final_dict)

def run(n):  # Number of equal parts
    partitions = list(zip(range(n),np.array_split(data.index, n)))
    p = Pool(processes=n)
    return_data = p.map(merge1, partitions)
    p.close()
    return pd.concat(return_data)

def merge2(data):
    loci_dict = {"A":["A1","A2"],"B":["B1","B2"],"C":["C1","C2"],"DRB1":["DRB1_1","DRB1_2"],"DQB1":["DQB1_1","DQB1_2"]}

    alleles_dict = {}
    for locus in loci_dict:
        alleles_locus = set(sorted(data[loci_dict[locus][0]].dropna().values.tolist() + data[loci_dict[locus][1]].dropna().values.tolist()))
        alleles_dict[locus] = {}
        n = 1
        for allele in alleles_locus:
            alleles_dict[locus][allele] = n
            n += 1

    final = pd.DataFrame(data[["ID","type","loci",'generation']])
    original = pd.DataFrame(data[["ID","type","loci",'generation']])
    for locus in loci_dict.keys():
        final[locus] = data[loci_dict[locus]].apply(lambda x: set(sorted([alleles_dict[locus][i] for i in x if i in alleles_dict[locus]])), axis=1)
        original[locus] = data[loci_dict[locus]].apply(lambda x: set(sorted([i for i in x if i in alleles_dict[locus]])), axis=1)
    print(final)
    final.reset_index(drop=True).to_pickle("all.pickle")
    original.reset_index(drop=True).to_pickle("all_original.pickle")

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--threads','-t', type=int, help='Number of threads to use', required=True)

args = parser.parse_args()


file = "data/Extra_Analyses_Greek_CBUs_BMDs_80804_noD_no124.xlsx"
data = pd.read_excel(file)[['ID','TYPE','GENERATION','A1_GROUPED','A2_GROUPED','B1_GROUPED','B2_GROUPED','C1_GROUPED','C2_GROUPED','DRB1_1_GROUPED','DRB1_2_GROUPED','DQB1_1_GROUPED','DQB1_2_GROUPED']]
data.columns = ['ID',"TYPE",'GENERATION','A1','A2','B1','B2','C1','C2','DRB1_1','DRB1_2','DQB1_1','DQB1_2']

final = run(args.threads)
merge2(final)