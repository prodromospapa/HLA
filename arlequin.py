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
    pattern = re.compile(r'== Sample : 	(.*?\.xlsx).*?== .*? : .*?</Reference>\n<data>(.*?)</data>.*?</Reference>\n<data>(.*?)</data>', re.DOTALL)
    # Find all non-overlapping matches of the regex pattern in the content
    matches = pattern.findall(content)
    # Extract the first value of each sublist as the key and the next two values as the values
    xlsx_files = [sublist[0] for sublist in matches]
    result_dict = [{"LD":[i.strip() for i in sublist[1].split("\n") if i!=""],"HWE":[i.strip() for i in sublist[2].split("\n") if i!=""]} for sublist in matches]

    #if multiple xlsx files are present in the output file then ask the user to select the file
    xlsx = 0
    if len(xlsx_files) > 1:
        question = dict(zip(range(len(xlsx_files)),xlsx_files))
        xlsx = int(input(f"Enter the xlsx file index {question}: "))

    test_dict = {"LD":["ld","LD","Pairwise linkage disequilibrium"],
                 "HWE":["hw","HW","Hardy-Weinberg equilibrium"]}
    if test in test_dict["LD"]:
        return LD(result_dict[xlsx]["LD"])
    elif test in test_dict["HWE"]:
        return HW(result_dict[xlsx]["HWE"])    
    

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--test','-t', type=str, help='Test to include in the ARP file')
args = parser.parse_args()

pprint(return_data("output.res/output.xml",args.test))