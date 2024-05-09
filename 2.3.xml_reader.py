import xml.etree.ElementTree as ET
import pandas as pd
import argparse
import re
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def HWE(data):
    headers = ['Locus', '#Genot', 'Obs.Het.', 'Exp.Het.', 'P-value', 's.d.', 'Steps done']
    df_data = [i.split() for i in data.split("\n")[9:-4]]
    df_data = [i for i in df_data if len(i)>1]
    df = pd.DataFrame(df_data, columns=headers)
    df = df.set_index("Locus")
    return df

def AMOVA(input_dict):
    return_dict = {}
    
    # Extract the AMOVA results for each locus
    input_text = input_dict["loci"]
    # Define regular expressions for the sections to extract
    amo = re.compile(r"AMOVA Results for polymorphic loci only:(.*?)Global AMOVA results as a weighted average over loci", re.DOTALL)
    global_amo = re.compile(r"Global AMOVA results as a weighted average over loci(.*?)Significance tests", re.DOTALL)

    amo_results = amo.search(input_text).group(1).strip()
    global_amo_results = global_amo.search(input_text).group(1).strip()

    # Extract the data for each locus
    dict_per_locus = {}
    per_locus = amo_results.split("\n")[4:-2]
    data = [i.split()[1:] for i in per_locus]
    locus = list(range(1,len(data)+1))
    if args.total:
        header = ["SSD", "d.f.", "Va", "% variation", "SSD", "d.f.", "Vb", "% variation", "FIS", "P-value"]
        parts = [["Among Individuals",[0,4]],["Withing Individuals",[4,8]],["Fixation index",[8,10]]]
    else:
        header =  ["SSD", "d.f.", "Va", "% variation", "SSD", "d.f.", "Vb", "% variation", "SSD", "d.f.", "Vc", "% variation", "FIS", "P-value", "FST", "P-value", "FIT", "P-value"]
        parts = [["Among populations",[0,4]],["Among individuals within populations",[4,8]],["Withing populations",[8,12]],["Fixation index",[12,18]]]
    df = pd.DataFrame(data, columns=header)
    for part,indeces in parts:
        new_df = df.iloc[:,indeces[0]:indeces[1]].copy()
        new_df["Locus"] = locus
        new_df.set_index("Locus",inplace=True)
        dict_per_locus[part] = new_df

    # Extract the global AMOVA results
    if args.total:
        df_global_amo = pd.DataFrame(['Among individuals ','Within Individuals',"Total"], columns=["Source of Variation"])
        df_global_amo = df_global_amo.set_index("Source of Variation")
        header = ["Sum of Squares", "Variance Components", "% variation"]
        df_global_amo[header] = pd.DataFrame([i.split()[1:] for i in global_amo_results.split("\n")[11:17] if i.split()[1:]],index=df_global_amo.index)
    else:
        df_global_amo = pd.DataFrame(['Among populations','Among individuals within populations ','Withing populations',"Total"], columns=["Source of Variation"])
        df_global_amo = df_global_amo.set_index("Source of Variation")
        header = ["Sum of Squares", "Variance Components", "% variation"]
        df_global_amo[header] = pd.DataFrame([i.split()[1:] for i in global_amo_results.split("\n")[11:22] if i.split()[1:]],index=df_global_amo.index)

    # Extract the FST, FIT and FIS values
    fst = {}
    if args.total:
        data = [global_amo_results.split("\n")[21]]
    else:
        data = global_amo_results.split("\n")[27:30]
    for item in data:
        key, value = item.split(':')
        fst[key.strip()] = float(value.strip())
    loci = [dict_per_locus, df_global_amo, fst]

    # Extract the AMOVA results for each population
    pop = {}
    input_text = input_dict["pop"].split("\n\n")[2:4]
    header = re.split(r'\s{2,}',input_text[0].split("\n")[3])[1:]
    for i in [["pop",0],["pop_per",1]]:
        pattern = r'[-+]?\d*\.\d+|[-+]?\d+'
        data= [re.findall(pattern,i) for i in input_text[i[1]].split("\n")[5:-1]]
        df = pd.DataFrame(data,columns=header)
        pop[i[0]] = df.set_index("Locus")

    return loci, pop

def LD(text):
    matches = re.split(r'Loci \d+ and \d+', text)
    pairs = re.findall(r'(Loci \d+ and \d+)', text)
    basic_stats = LD_stats(matches[0])
    pair_dict={}
    for pair,stats in zip(pairs, matches[1:]):
        stats_dict = {}
        stats_list = re.split(r"\d+: ", stats)[1:]
        for stat_itter in stats_list:
            splitter = stat_itter.split("\n\n")
            stat_name = splitter[0]
            stat_text = splitter[1].split("\n")
            if stat_name == 'Observed contingency table':
                stat_text = stat_text[:-1]            

            stats_dict[stat_name] = LD_text2table(stat_name,stat_text)
        pair_dict[pair] = stats_dict
    return pair_dict, basic_stats

def LD_text2table(stat_name,stat_text):
    header = [i.strip() for i in stat_text[0].split("|")]
    rows = []
    if stat_name == 'Observed contingency table':
        for row in stat_text[1:]:
            rows.append([i.strip() for i in row.split("|")])
        header[-1] = "Total"
        rows[-1][0] = "Total"
    else:
        header = header[:-1]
        for row in stat_text[1:]:
            rows.append([i.strip() for i in row.split("|")[:-1]])
        
    table = pd.DataFrame(rows, columns=header)
    table = table.set_index(header[0])
    with pd.option_context("future.no_silent_downcasting", True):
        table.replace("",np.nan,inplace=True)
    return table.astype(float)

def LD_stats(basic_stats):
    stats = {}
    basic_stats = basic_stats.split("\n\n")

    #p values
    pattern = re.compile(r"Pair \((\d+,\s+\d+)\)\s+Exact\s+P=([\d.]+)\s+\+\-\s+([\d.]+)\s+\(([\d]+)\s+Steps done\)")
    df = pd.DataFrame([re.search(pattern,i).groups() for i in basic_stats[2].split("\n")],columns=["Pair","P-value","s.d.","Steps done"])
    df = df.set_index("Pair")
    stats["p_values"] = df

    #Table of significant linkage disequilibrium (significance level=0.005)
    data = basic_stats[4].split("\n")
    columns = [i.strip() for i in data[1].split("|")[:-1]]
    data = [[i.split("|")[0]] + [j.strip() for j in i.split("|")[1].split("   ")] for i in data[3:]]
    df = pd.DataFrame(data, columns=columns)
    df = df.set_index(columns[0])
    stats["significant_LD"] = df

    
    for i,j in [[5,1],[7,2]]:
        data = basic_stats[i].split("\n")[j:]
        headers = data[1].split()[:-3] + ["No. of Loci"]
        rows = [row.split() for row in data[3::2]]
        df = pd.DataFrame(rows, columns=headers)
        df = df.set_index(headers[0])
        if i == 5:
            #Number of linked loci per polymorphic locus (significance level=0.005)
            stats["linked_loci"] = df
        else:
            #Percentage of linked loci per locus (significance level=0.005)
            stats["linked_loci_per_locus"] = df
    return stats

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--test','-t',choices=["HWE","LD","AMOVA"], type=str, help='Test to include in the ARP file',required=True)
parser.add_argument('--loci','-l', type=str,choices=['3','5'], help='Number of loci',required='-d'=="Greece")
parser.add_argument('--database','-d', type=str,choices=["Greece","DKMS"], help='database to use', required=True)
parser.add_argument('--total','-to', action='store_true', help='Total of database', required=False)

args = parser.parse_args()

if args.total:
    total = "_total"
else:
    total = ""
if args.database == "Greece":
    if args.loci == None:
        raise argparse.ArgumentTypeError("the following arguments are required: --loci/-l")
    file = f"output/output_{args.loci}{total}.res/output_{args.loci}{total}.xml"
else:
    file = f"output/output_dkms{total}.res/output_dkms{total}.xml"

# Parse the XML file
tree = ET.parse(file)

# Get the root element
root = tree.getroot()
# Access elements and attributes in the XML file
check =""
info = {}

for i in range(len(root)):
    if "NAME" in root[i].attrib.keys():
        if (root[i+1].tag == "data") and "group" in root[i].attrib['NAME']:
            name = re.search(r"Sample\s*:\s*(\w+)", root[i+1].text).group(1)
            info[name] = {"LD":root[i+5].text,"HWE":root[i+8].text}
        elif (root[i+1].tag == "data"):
            if root[i].attrib["NAME"].endswith("pop_Loc_by_Loc_AMOVA"):
                info["AMOVA"] = {"loci":root[i+1].text,"pop":root[i+3].text}
            
def heatmap(table,pair,bank):
    sns.heatmap(table, cmap="coolwarm")
    pattern = r"Loci (\d+) and (\d+)"
    loci = re.search(pattern,pair).groups()
    loci_list = ["A","B","C","DRB1","DQB1"]
    plt.title("LD Heatmap")
    plt.xlabel(f"Locus {loci_list[int(loci[0])]}")
    plt.ylabel(f"Locus {loci_list[int(loci[1])]}")
    plt.tight_layout()
    pair = loci_list[int(loci[0])] + "_" + loci_list[int(loci[1])]
    plt.savefig(f"plots/{bank}_{pair}.png")
    plt.close()





if args.test == "AMOVA":
    loci,pop = AMOVA(info["AMOVA"])
    #pprint(loci)
    #pprint(pop)

else:
    banks = list(info.keys())[:-1]
    #bank = input("Choose a bank: " + ", ".join(banks) + "\n")
    if args.test == "HWE":
        hwe = HWE(info[bank]["HWE"])
        #print(hwe)
    elif args.test == "LD":
        for bank in banks:
            pair_dict, basic_stats = LD(info[bank]["LD"])
            pairs = pair_dict.keys()
            for pair in pairs:
                table = pair_dict[pair]["Table of standardized disequilibrium values (D'=D/Dmax)"]
                heatmap(table,pair,bank)
        #pprint(pair_dict)
        #pprint(basic_stats)

    
