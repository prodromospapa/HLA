import re
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import argparse
import os
from multiprocessing import Pool

def freq(xml):
    tree = ET.parse(xml)
    root = tree.getroot()
    for i in range(len(root)):
        my_key = root[i].attrib
        if ("NAME" in my_key.keys()) and ("group" in my_key['NAME']):
            data = root[i+7].text.split("\n")
            final = []
            for d in data:
                if d:
                    text = d.strip()
                    if text[0].isnumeric():
                        text = text.split("  ")
                        final.append([float(text[1]),text[4]])
    final = pd.DataFrame(final,columns=["Freq.","Haplotype"])
    final["Freq."] = [i/sum(final["Freq."]) for i in final["Freq."]]
    return final

def bootstrap(samples,population_n):
    weights = np.array(samples["Freq."])
    hapl = np.array(samples["Haplotype"])
    data = np.random.choice(hapl, 2*population_n, p=weights, replace=True)
    data = [data[i:i+2] for i in range(0, len(data), 2)]
    return data

def sample2arp(samples,bootstrap_n):
    arp_content = f'''[Profile]

    Title="Genetic Data"
    NbSamples=1
    GenotypicData=1
    GameticPhase=1
    DataType=STANDARD 
    LocusSeparator=TAB 
    RecessiveData=0
    MissingData='?'

[Data]

[[Samples]]
'''
    counter = 0
    data = bootstrap(samples,bootstrap_n)
    arp_content += f'''SampleName="Bootstrap"
    SampleSize={len(data)}
    SampleData= {{
'''
    for row in data:
        counter +=1
        id = "Greece_"+str(counter)
        arp_content += f"{id}\t" + f"1\t" + row[0] + "\n" + "\t" + row[1] + "\n"
    arp_content += "}\n\n"
    arp_content += '''[[Structure]]
    StructureName="Simulated data"
    NbGroups=1
    Group={
    "Bootstrap"
    }'''
    return arp_content

def bootstrap2arp(lista):
    counter = 0
    bootstraps = lista[1]
    part = lista[0]
    for n in bootstraps:
        if not os.path.exists(f"bootstrap/bootstrap_{args.loci}/bootstrap_{args.loci}_{n}"):
            os.makedirs(f"bootstrap/bootstrap_{args.loci}/bootstrap_{args.loci}_{n}")
        for i in range(args.perm):
            if part == 0:
                counter +=1
                print(f"{counter}/{args.perm*len(bootstraps)}",end="\r")
            file = f"bootstrap/bootstrap_{args.loci}/bootstrap_{args.loci}_{n}/bootstrap_{args.loci}_{i}.arp"
            if not os.path.isfile(file):
                with open(file, 'w') as arp_file:
                    arp_file.write(sample2arp(samples,n))



def run(threads,bootstraps):  # Number of equal parts
    partitions = list(zip(range(threads),np.array_split(bootstraps,threads)))
    p = Pool(processes=threads)
    p.map(bootstrap2arp, partitions)

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--loci','-l', type=str,choices=['3','5'], help='Number of loci',required=True)
parser.add_argument('--perm','-p', type=int, help='Number of permutations', required=True)
parser.add_argument('--bootstrap','-b', type=str, help='Number of bootstrap samples', required=True)
parser.add_argument('--threads','-t', type=int, help='Number of threads to use', required=True)

args = parser.parse_args()

xml = f"bootstrap/bootstrap_{args.loci}.res/bootstrap_{args.loci}.xml"
samples = freq(xml)
total_table = pd.read_pickle("all_original_unmerged.pickle")
total_table = total_table[total_table['type']=="CBU"]

if not os.path.exists(f"bootstrap/bootstrap_{args.loci}"):
    os.makedirs(f"bootstrap/bootstrap_{args.loci}")

counter = 0
bootlist = [int(i) for i in args.bootstrap.split(",")]
bootstraps = range(bootlist[0],bootlist[1]+1)

run(args.threads,bootstraps)



