import re
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import argparse
import os

def freq(xml):
    tree = ET.parse(xml)
    root = tree.getroot()
    info = {}   
    header = ["No.","Freq.","s.d.","Haplotype"]
    for i in range(len(root)):
        my_key = root[i].attrib
        if ("NAME" in my_key.keys()) and ("group" in my_key['NAME']):
            name = re.search(r"Sample\s*:\s*(\w+)", root[i+1].text).group(1)
            data = root[i+7].text.split("\n")
            final = []
            for d in data:
                if d:
                    text = d.strip()
                    if text[0].isnumeric():
                        text = text.split("  ")
                        del text[3]
                        text[3] = text[3][1:]
                        final.append(text)
            df = pd.DataFrame(final,columns=header)
            df.set_index("No.",inplace=True)
            info[name] = df
    return info

def bootstrap(samples,population_n):
    weights = np.array(samples["Freq."].astype(float))
    weights = [i/sum(weights) for i in weights]
    hapl = np.array(samples["Haplotype"])
    data = np.random.choice(hapl, 2*population_n, p=weights, replace=True)
    data = [data[i:i+2] for i in range(0, len(data), 2)]
    return data

def sample2arp(samples,banks):
    population_n_dict = {}
    if args.database == "Greece":
        if args.total:
            population_n = total_table.shape[0]
        else:
            for bank in banks:
                population_n_dict[bank] = total_table[total_table['bank']==bank].shape[0]
    else:
        if args.total:
            population_n = total_table.shape[0]
        else:
            for bank in banks:
                population_n_dict[bank] = total_table[total_table['bank']==bank].shape[0]
    banks = list(samples.keys())
    if args.total:
        nbsample = 1
    else:
        nbsample = len(banks)

    arp_content = f'''[Profile]

    Title="Genetic Data"
    NbSamples={nbsample}
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
    if args.total:
        name = bank[0]
        data = bootstrap(samples[name],population_n)
        arp_content += f'''SampleName="{args.database}"
    SampleSize={len(data)}
    SampleData= {{
'''
        for row in data.iterrows():
            counter +=1
            id = str(counter)
            arp_content += f"{id}\t" + f"1\t" + row[0] + "\n" + "\t" + row[1] + "\n"
        arp_content += "}\n\n"
        arp_content += '''[[Structure]]
    StructureName="Simulated data"
    NbGroups=1
    Group={
    "Bootstrap"
    }'''
    else:
        for bank in banks:
            population_n = population_n_dict[bank]
            data_loop = bootstrap(samples[bank],population_n)
            arp_content += f'''SampleName="{bank}"
    SampleSize={len(data_loop)}
    SampleData= {{
    '''
            for row in data_loop:
                counter +=1
                id = bank+ "_" +str(counter)
                arp_content += f"{id}\t" + f"1\t" + row[0] + "\n" + "\t" + row[1] + "\n"
            arp_content += "}\n\n"
        arp_content += f'''[[Structure]]
    StructureName="Simulated data"
    NbGroups=1
    Group={{
    '''
        for bank in banks:
            arp_content+=f'    "{bank}"\n'
        arp_content += '}'
    return arp_content


parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--loci','-l', type=str,choices=['3','5'], help='Number of loci',required='-d'=="Greece")
parser.add_argument('--database','-d', type=str,choices=["Greece","DKMS"], help='database to use', required=True)
parser.add_argument('--total','-to', action='store_true', help='Total of database', required=False)
parser.add_argument('--perm','-p', type=int, help='Number of permutations', required=True)

args = parser.parse_args()

if args.total:
    total = "_total"
else:
    total = ""

if args.database == "Greece":
    xml = f"bootstrap/output_{args.loci}{total}.res/output_{args.loci}{total}.xml"
    samples = freq(xml)
else:
    xml = f"bootstrap/output_dkms{total}.res/output_dkms{total}.xml"
    samples = freq(xml)

banks = list(samples.keys())

if args.database == "Greece":
    total_table = pd.read_pickle("all_original_unmerged.pickle")
else:
    total_table = pd.read_pickle("dkms.pkl")

if not os.path.exists(f"bootstrap/bootstrap_{args.loci}{total}"):
    os.makedirs(f"bootstrap/bootstrap_{args.loci}{total}")
counter = 0
for i in range(args.perm):
    counter +=1
    print(f"{counter}/{args.perm}",end="\r")
    with open(f'bootstrap/bootstrap_{args.loci}{total}/bootstrap_{args.loci}{total}_{i}.arp', 'w') as arp_file:
        arp_file.write(sample2arp(samples,banks))



