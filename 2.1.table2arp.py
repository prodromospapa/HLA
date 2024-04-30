import pandas as pd
import argparse
import os


def xl2arp(data_h_l):
    fst_n = len(counter_dict)
    hl_n = len(data_h_l)
    # Initialize the ARP file content
    arp_content_fst = arp_content_h_l = f'''[Profile]

    Title="Genetic Data from Greek Populations"'''

    arp_content_fst += f'''
    NbSamples={fst_n}
    GenotypicData=1
    GameticPhase=1
    DataType=STANDARD 
    LocusSeparator=TAB 
    RecessiveData=0
    MissingData='?'

[Data]

[[Samples]]

'''
    

    arp_content_h_l += '''
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
    arp_content_h_l += f'''SampleName="Greece"
SampleSize={hl_n}
SampleData= {{
'''

    counter = 0
    total = len(data_h_l)
    structure = ""
    checker = [] # To check if the same sample has been added to the ARP file for the FST
    for index, row in data_h_l.iterrows():
        counter +=1
        #fst
        name_id_fst = dict_key_fst = tuple(row[loci_list])
        n_fst = counter_dict[dict_key_fst]
        name_fst = counter
        #hl
        name_hl = f"{row['ID']}"
        if loci == '3':
            loci_l = [['A1','B1','DRB1_1'],['A2','B2','DRB1_2']]
        else:
            loci_l = [['A1','B1','C1','DRB1_1','DQB1_1'],['A2','B2','C2','DRB1_2','DQB1_2']]
        arp_content_h_l += f"{name_hl}\t" + f"1\t" + '\t'.join(row[loci_l[0]]) + "\n" + "\t" + '\t'.join(row[loci_l[1]]) + "\n"
        if name_id_fst not in checker:
            arp_content_fst += f'''SampleName="{name_id_fst}"\nSampleSize={n_fst}\nSampleData= {{\n{name_fst}\t''' + f"{n_fst}\t" + '\t'.join(row[loci_l[0]]) + "\n" + "\t" + '\t'.join(row[loci_l[1]]) + "}\n\n"
            structure += f'\t"{name_id_fst}"\n'
            checker.append(name_id_fst)
        print(f"{counter}/{total}",end="\r")

    # Write the ARP file
    arp_content_h_l += "}\n\n"

    arp_content_fst +=f'''[[Structure]]

	StructureName="New Edited Structure"
	NbGroups=1

	Group={{
{structure}
	}}
    '''
    
    return arp_content_h_l, arp_content_fst
    
parser = argparse.ArgumentParser(description='Convert excel file to arlequin format')
parser.add_argument('--loci','-l', type=str,choices=['3','5','all'], help='Number of loci',required=True)

args = parser.parse_args()

loci = args.loci
input = "all_original_unmerged.pickle"

# Create the output folder if it doesn't exist
if not os.path.exists('output'):
    os.makedirs('output')

if loci == '3':
    loci_list = ["A1","A2","B1","B2","DRB1_1","DRB1_2"]
    data_h_l = pd.read_pickle(input)[["ID"]+loci_list]
    data_fst = data_h_l.drop_duplicates(subset=loci_list)
    counter_dict = dict(data_h_l[loci_list].value_counts())

    arp_content_h_l, arp_content_fst = xl2arp(data_h_l)
    with open(f'output/output_h_l_{loci}.arp', 'w') as arp_file:
        arp_file.write(arp_content_h_l)
    with open(f'output/output_amova_{loci}.arp', 'w') as arp_file:
        arp_file.write(arp_content_fst)

elif loci == '5':
    loci_list = ["A1","A2","B1","B2","C1","C2","DRB1_1","DRB1_2","DQB1_1","DQB1_2"]
    data = pd.read_pickle(input)
    data_h_l = data[data['loci']==5][["ID"]+loci_list]
    data_fst = data_h_l.drop_duplicates(subset=loci_list)
    counter_dict = dict(data_h_l[loci_list].value_counts())

    arp_content_h_l, arp_content_fst = xl2arp(data_h_l)
    with open(f'output/output_h_l_{loci}.arp', 'w') as arp_file:
        arp_file.write(arp_content_h_l)
    with open(f'output/output_amova_{loci}.arp', 'w') as arp_file:
        arp_file.write(arp_content_fst)

else:
    loci_list = ["A1","A2","B1","B2","C1","C2","DRB1_1","DRB1_2","DQB1_1","DQB1_2"]
    data_h_l = pd.read_pickle(input)[["ID"]+loci_list].fillna('?')
    data_fst = data_h_l.drop_duplicates(subset=loci_list)
    counter_dict = dict(data_h_l[loci_list].value_counts())

    arp_content_h_l, arp_content_fst = xl2arp(data_h_l)
    with open(f'output/output_h_l.arp', 'w') as arp_file:
        arp_file.write(arp_content_h_l)
    with open(f'output/output_amova.arp', 'w') as arp_file:
        arp_file.write(arp_content_fst)

# python3 2.1.table2arp.py -l 3
