import re
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import argparse
import os
from multiprocessing import Pool


def HWE(data):
    headers = ['Locus', '#Genot', 'Obs.Het.', 'Exp.Het.', 'P-value', 's.d.', 'Steps done']
    df_data = [i.split() for i in data.split("\n")[9:-4]]
    df_data = [i for i in df_data if len(i)>1]
    df = pd.DataFrame(df_data, columns=headers)
    df = df.set_index("Locus")
    p_value = df["P-value"].astype(float)
    average_p_value = p_value.mean()
    return average_p_value

def AMOVA(input_text):
    data = input_text.split("\n\n")[2].split("\n")
    header = re.split(r'\s{2,}', data[3])[1:]
    df = pd.DataFrame([i.split() for i in data[5:-1]], columns=header)
    fis = df.iloc[:,2:].astype(float)
    average = np.array(fis.mean().tolist())
    return average

def run_arl(input_text):
    os.system(f"bash arlecore_linux/LaunchArlecore.sh {input_text} BOOT > /dev/null")

def read_stats(file):
    tree = ET.parse(file)
    root = tree.getroot()
    hwe = np.array([])
    for i in range(len(root)):
        if "NAME" in root[i].attrib.keys():
            if (root[i+1].tag == "data") and "group" in root[i].attrib['NAME']:
                input_text = root[i+4].text
                hwe = np.append(hwe,HWE(input_text))
            elif (root[i+1].tag == "data"):
                if root[i].attrib["NAME"].endswith("comp_sum_LBL_POP_AMOVA_FIS"):
                    fst_input = root[i+1].text
    fst = AMOVA(fst_input)
    return hwe, fst

def run(threads,bootstrap_folders):  # Number of equal parts
    partitions = list(zip(range(threads),np.array_split(bootstrap_folders, threads)))
    p = Pool(processes=threads)
    return_data = p.map(stats, partitions)
    p.close()
    df = pd.concat(return_data)
    return df.sort_index()

def stats(partition):
    part, bootstraps_folders = partition
    df = pd.DataFrame(columns=["HWE","FST"],index=[int(i.split("_")[-1]) for i in bootstraps_folders])
    counter = 0
    total = len(bootstraps_folders)*sum([1 for i in os.listdir(f"bootstrap/bootstrap_{args.loci}/{bootstraps_folders[0]}") if i.endswith(".arp")])
    for bootstrap in bootstraps_folders:
        folder = f"bootstrap/bootstrap_{args.loci}/{bootstrap}" 
        bootstrap_n = int(bootstrap.split("_")[-1])
        hwe_list = []
        fst_list = []
        for file in os.listdir(folder):
            if file.endswith(".arp"):     
                file_dir = folder+"/"+file
                xml = file_dir.replace(".arp",".res")+f"/{file.replace('.arp','')}.xml"
                if not os.path.isfile(xml):
                    run_arl(file_dir)
                try:
                    hwe, fst = read_stats(xml)
                except Exception:
                    run_arl(file_dir)
                hwe_list = np.append(hwe > obs_hwe,hwe_list)
                fst_list = np.append(fst > obs_fst,fst_list)
                if part == 0:
                    counter += 1
                    print(f"{counter}/{total}",end="\r")
        df.loc[bootstrap_n] = [sum(hwe_list)/len(hwe_list),sum(fst_list)/len(fst_list)] 
    return df

parser = argparse.ArgumentParser(description='ARP file generator')
parser.add_argument('--loci','-l', type=str,choices=['3','5'], help='Number of loci',required=True)
parser.add_argument('--threads','-t', type=int, help='Number of threads',required=True)


args = parser.parse_args()


#observed
run_arl(f"bootstrap/bootstrap_{args.loci}.arp")
obs_hwe, obs_fst = read_stats(f"bootstrap/bootstrap_{args.loci}.res/bootstrap_{args.loci}.xml")

#bootstrap
bootstraps_folders =[i for i in os.listdir(f"bootstrap/bootstrap_{args.loci}")]
df = run(args.threads,bootstraps_folders)
df.index.name = "Bootstrap"
print(df)



