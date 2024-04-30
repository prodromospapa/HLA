import xml.etree.ElementTree as ET
import pandas as pd
from pprint import pprint
import argparse
import re

def HWE(data):
    headers = ['Locus', '#Genot', 'Obs.Het.', 'Exp.Het.', 'P-value', 's.d.', 'Steps done']
    df_data = [i.split() for i in data[7:-13]]
    df = pd.DataFrame(df_data, columns=headers)
    df = df.set_index("Locus")
    print(df)
    return df

def AMOVA(input_text):
    # Define regular expressions for the sections to extract
    amo = re.compile(r"AMOVA Results for polymorphic loci only:(.*?)Global AMOVA results as a weighted average over loci", re.DOTALL)
    global_amo = re.compile(r"Global AMOVA results as a weighted average over loci(.*?)END OF RUN", re.DOTALL)

    amo_results = amo.search(input_text).group(1).strip()
    global_amo_results = global_amo.search(input_text).group(1).strip()

    # Extract the data for each locus
    per_locus = amo_results.split("\n")[4:-2]
    header =  ["Locus", "SSD", "d.f.", "Va", "% variation", "SSD", "d.f.", "Vb", "% variation", "SSD", "d.f.", "Vc", "% variation", "FIS", "P-value", "FST", "P-value", "FIT", "P-value"]
    df_per_locus = pd.DataFrame([i.split() for i in per_locus], columns=header)
    df_per_locus.set_index("Locus", inplace=True)

    # Extract the global AMOVA results
    df_global_amo = pd.DataFrame(['Among populations','Among individuals within populations ','Withing populations',"Total"], columns=["Source of Variation"])
    df_global_amo = df_global_amo.set_index("Source of Variation")
    header = ["Sum of Squares", "Variance Components", "% variation"]
    df_global_amo[header] = pd.DataFrame([i.split()[1:] for i in global_amo_results.split("\n")[11:-28] if i.split()[1:]],index=df_global_amo.index)

    # Extract the FST, FIT and FIS values
    fst = {}
    for item in global_amo_results.split("\n")[-23:-20]:
        key, value = item.split(':')
        fst[key.strip()] = float(value.strip())
    print(df_per_locus, df_global_amo, fst)
    return df_per_locus, df_global_amo, fst

#def LD(element):

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--test','-t',choices=["HWE","LD","AMOVA"], type=str, help='Test to include in the ARP file',required=True)
parser.add_argument('--loci','-l', type=str,choices=['3','5','A','B','C','DRB1','DQB1','all'], help='Number of loci',required=True)

args = parser.parse_args()

if args.test == "AMOVA":
    file = f"output/output_amova_{args.loci}.res/output_amova_{args.loci}.xml"
else:
    file = f"output/output_h_l_{args.loci}.res/output_h_l_{args.loci}.xml"

# Parse the XML file
tree = ET.parse(file)

# Get the root element
root = tree.getroot()
# Access elements and attributes in the XML file
for element in root:
    if args.test == "HWE":
        if element.tag == "data":
            data = element.text.strip().split("\n")
            if data[0].startswith("Exact test using a Markov chain (for all Loci):"):
                HWE(data)
    elif args.test == "AMOVA":
        if "NAME" in element.attrib.keys():
            check = element.attrib['NAME'].endswith("pop_Loc_by_Loc_AMOVA")
            if element.tag == "data" and check:
                input_text = element.text
                AMOVA(input_text)
    elif args.test == "LD":
        if element.tag=="data":
            data = element.text.strip().split("\n")
            if data[0].startswith("Test of linkage disequilibrium for all pairs of loci:"):
                print(data)