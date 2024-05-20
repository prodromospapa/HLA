import re
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import argparse
import os
from pprint import pprint


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
    df = df.set_index("Locus")
    fis = df["Average FIS"].astype(float)
    average_p_value = fis.mean()
    return average_p_value


def run_arl(input_text):
    os.system(f"bash arlecore_linux/LaunchArlecore.sh {input_text} BOOT")

def read_stats(file,obs):
    tree = ET.parse(file)
    root = tree.getroot()
    info = {}
    for i in range(len(root)):
        if "NAME" in root[i].attrib.keys():
            if (root[i+1].tag == "data") and "group" in root[i].attrib['NAME']:
                name = re.search(r"Sample\s*:\s*(\w+)", root[i+1].text).group(1)
                if obs:
                    info["HWE"] = root[i+8].text
                else:
                    info["HWE"] = root[i+4].text
            elif (root[i+1].tag == "data"):
                if root[i].attrib["NAME"].endswith("comp_sum_LBL_POP_AMOVA_FIS"):
                    info["AMOVA"] = root[i+1].text
    hwe = HWE(info["HWE"])
    fst = AMOVA(info["AMOVA"])
    return hwe, fst

parser = argparse.ArgumentParser(description='ARP file generator')
parser.add_argument('--database','-d', type=str,choices=["Greece","DKMS"], help='database to use', required=True)
parser.add_argument('--loci','-l', type=str,choices=['3','5'], help='Number of loci',required='-d'=="Greece")
parser.add_argument('--total','-to', action='store_true', help='Total of database', required=False)

args = parser.parse_args()

if args.total:
    total = "_total"
else:
    total = ""

#observed
obs_xml = f"output/output_{args.loci}{total}.res/output_{args.loci}{total}.xml"
obs_hwe, obs_fst = read_stats(obs_xml,True)


folder = f"bootstrap/bootstrap_{args.loci}{total}"
info = {}
files =[i for i in os.listdir(folder) if i.endswith(".arp")]
total = len(files)
counter = 0
for file in files:
    counter += 1
    info[counter] = {"HWE":[],"FIS":[]}
    file_dir = folder+"/"+file
    xml = file_dir.replace(".arp",".res")+f"/{file.replace('.arp','')}.xml"
    if not os.path.isfile(xml):
        run_arl(file_dir)
    try:
        hwe, fst = read_stats(xml,False)
    except Exception:
        run_arl(file_dir)
    info[counter]["HWE"].append(hwe)
    info[counter]["FIS"].append(fst)
    print(f"{counter}/{total}",end="\r")
print(info)


