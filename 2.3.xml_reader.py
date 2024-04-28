import re
import pandas as pd
import re
import argparse
from pprint import pprint

def LD(data): #replace 
    pair_data = {}
    for i in range(len(data)):
        if data[i].startswith("Pair"):
            pair_key = data[i]
            values_1 = [float(i.split(":")[1].strip()) for i in data[i+1].strip().split("          ")]  #LnLHood LD, LnLHood LE
            values_2 = data[i+2].strip().split("     ")
            p = values_2[0].split("=")[1]#value, +- error, permutation
            x2 = values_2[1].split("e=")[1] #x2, p, df
            pattern  = r'\d+(?:\.\d+)?'
            values_2 = [[float(val) for val in re.findall(pattern, p)]] + [[float(val) for val in re.findall(pattern, x2)]] #Exact P, Chi-square test 
            pair_data[pair_key] = values_1 + values_2
            #convert dictionary to dataframe
            df_pair = pd.DataFrame(pair_data).T
            df_pair.columns = ['LnLHood LD', 'LnLHood LE', 'Exact P', 'Chi-square test']

        elif data[i].startswith("Histogram of the number of linked loci per locus"):#same replace number with allele
            locus = data[i+2].split()[1:]
            number = [int(num) for num in data[i+4].split()]
            histogram = dict(zip(locus,number))

        elif data[i].startswith("Table of significant linkage disequilibrium"):
            last_number = data[i+2].split("|")[-2]
            table = [data[i+2]] + data[i+4:i+4+int(last_number)+1]

            #text2table
            headers = table[0].split('|')[1:]  # Split the string by '|' and take everything after the first item
            headers = [h.strip() for h in headers if h.strip()]  # Strip whitespace from each header and remove empty strings
            data_list = []
            for row in table[1:]:
                components = row.split('|')  # Split the row by '|'
                row_data = components[1].split()  # Take the data part and split by whitespace to get individual data points
                data_list.append(row_data)  # Add the processed row data to the data list
            df_singificant = pd.DataFrame(data_list, columns=headers)  # Create a DataFrame from the data and headers
            #text to table

    return df_pair, histogram, df_singificant

def HW(data):
    borders = []
    for i in range(len(data)):
        if data[i].startswith("---------------------"):
             borders.append(i)
    table = data[borders[1]+1:borders[2]]

    #text2table
    headers = ['Locus', '#Genot', 'Obs.Het.', 'Exp.Het.', 'P-value', 's.d.', 'Steps done']
    data = []
    for row in table:
        components = row.split()  # Split the row by blank space
        data.append(components)  # Add the processed row data to the data list
    df = pd.DataFrame(data, columns=headers)  # Create a DataFrame from the data and headers
    df.set_index('Locus', inplace=True)
    #text2table

    return df

def return_data(file_path,test):
    with open(file_path, 'r') as file:
        content = file.read()
    # This regex pattern looks for 'Reference' followed by any characters (non-greedy),
    # then 'data' and captures any characters until the next 'data'
    pattern = re.compile(r'== Sample : 	(.*?)\n.*?== .*? : .*?</Reference>\n<data>(.*?)</data>.*?</Reference>\n<data>(.*?)</data>', re.DOTALL)
    # Find all non-overlapping matches of the regex pattern in the content
    matches = pattern.findall(content)
    # Extract the first value of each sublist as the key and the next two values as the values
    result_dict = {"LD":[i.strip() for i in matches[0][1].split("\n") if i!=""],"HWE":[i.strip() for i in matches[0][2].split("\n") if i!=""]}


    if test == "LD":
        return LD(result_dict["LD"])
    elif test == "HWE":
        return HW(result_dict["HWE"])    

def parse_xml(xml_file):
    import xml.etree.ElementTree as ET
    
    # Parse the XML file
    tree = ET.parse(xml_file)

    # Get the root element
    root = tree.getroot()
    
    # Access elements and attributes in the XML file
    check = False
    for element in root:
        if "NAME" in element.attrib.keys():
            check = element.attrib['NAME'].endswith("pop_Loc_by_Loc_AMOVA")
        if element.tag == "data" and check:
            input_text = element.text

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

    return df_per_locus, df_global_amo, fst

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--test','-t',choices=["HWE","LD","AMOVA"], type=str, help='Test to include in the ARP file',required=True)
parser.add_argument('--loci','-l', type=str,choices=['3','5','A','B','C','DRB1','DQB1','all'], help='Number of loci',required=True)
parser.add_argument('--drop_double','-d', action='store_true', help='Drop double entries')

args = parser.parse_args()

if args.drop_double:
    add = "_no_d"
else:
    add = ""

if args.test == "AMOVA":
    file = f"output/output_amova_{args.loci}{add}.res/output_amova_{args.loci}{add}.xml"
    pprint(parse_xml(file))
else:
    file = f"output/output_h_l_{args.loci}{add}.res/output_h_l_{args.loci}{add}.xml"
    pprint(return_data(file,args.test))

# python3 2.2.xml_reader.py -t AMOVA -l 3 -d