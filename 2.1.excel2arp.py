import pandas as pd
import argparse
import os


def xl2arp(data):
    # Initialize the ARP file content
    arp_content_fst = arp_content_h_l = f'''[Profile]

    Title="Genetic Data from Greek Populations"'''

    if drop_double:
        fst_n = len(counter_dict)
        pop_n = sum(counter_dict.values())
    else:
        fst_n = len(data)
        
    arp_content_fst += f'''
    NbSamples={fst_n}
    GenotypicData=1
    GameticPhase=0
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
    GameticPhase=0
    DataType=STANDARD 
    LocusSeparator=TAB 
    RecessiveData=0
    MissingData='?'

[Data]

[[Samples]]

'''
    arp_content_h_l += f'''SampleName="Greece"
SampleSize={pop_n}
SampleData= {{
'''

    counter = 0
    total = len(data)
    structure = ""
    for index, row in data.iterrows():
        counter +=1
        if drop_double:
            if loci in ['A','B','C','DRB1','DQB1']:
                dict_key = tuple(row[loci_dict[loci]])
            else:
                dict_key = tuple(row[loci_list])
            n = counter_dict[dict_key]
            name = counter
            name_id = dict_key
        else:
            name_id = name = f"{row['ID']}"
            n = 1
        structure += f'\t"{name_id}"\n'
        if loci == '3':
            arp_content_h_l += f"{name}\t" + f"{n}\t" + '\t'.join(row[['A1','B1','DRB1_1']]) + "\n" + "\t" + '\t'.join(row[['A2','B2','DRB1_2']]) + "\n"
            arp_content_fst += f'''SampleName="{name_id}"\nSampleSize={n}\nSampleData= {{\n{name}\t''' + f"{n}\t" + '\t'.join(row[['A1','B1','DRB1_1']]) + "\n" + "\t" + '\t'.join(row[['A2','B2','DRB1_2']]) + "}\n\n"
        elif loci in ['A','B','C','DRB1','DQB1']:
            arp_content_h_l += f"{name}\t" + f"{n}\t" + row[loci_dict[loci][0]] + "\n" + "\t" + row[loci_dict[loci][1]] + "\n"
            arp_content_fst += f'''SampleName="{name_id}"\nSampleSize={n}\nSampleData= {{\n{name}\t''' + f"{n}\t" + row[loci_dict[loci][0]] + "\n" + "\t" + row[loci_dict[loci][1]] + "}\n\n"
        else:
            arp_content_h_l += f"{name}\t" + f"{n}\t" + '\t'.join(row[['A1','B1','C1','DRB1_1','DQB1_1']]) + "\n" + "\t" + '\t'.join(row[['A2','B2','C2','DRB1_2','DQB1_2']]) + "\n"
            arp_content_fst += f'''SampleName="{name_id}"\nSampleSize={n}\nSampleData= {{\n{name}\t''' + f"{n}\t" + '\t'.join(row[['A1','B1','C1','DRB1_1','DQB1_1']]) + "\n" + "\t" + '\t'.join(row[['A2','B2','C2','DRB1_2','DQB1_2']]) + "}\n\n"
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
parser.add_argument('--loci','-l', type=str,choices=['3','5','A','B','C','DRB1','DQB1','all'], help='Number of loci',required=True)
parser.add_argument('--drop_double','-d', action='store_true', help='Drop double entries')

args = parser.parse_args()

loci = args.loci
drop_double = args.drop_double
input = "all_original_unmerged.pickle"

# Create the output folder if it doesn't exist
if not os.path.exists('output'):
    os.makedirs('output')

if loci == '3':
    loci_list = ["A1","A2","B1","B2","DRB1_1","DRB1_2"]
    data = pd.read_pickle(input)[["ID"]+loci_list]
    if drop_double:
        counter_dict = dict(data[loci_list].value_counts())
        data = data.drop_duplicates(subset=loci_list)
        name_d = "_no_d"
    arp_content_h_l, arp_content_fst = xl2arp(data)
    with open(f'output/output_h_l_{loci}{name_d}.arp', 'w') as arp_file:
        arp_file.write(arp_content_h_l)
    with open(f'output/output_amova_{loci}{name_d}.arp', 'w') as arp_file:
        arp_file.write(arp_content_fst)

elif loci == '5':
    loci_list = ["A1","A2","B1","B2","C1","C2","DRB1_1","DRB1_2","DQB1_1","DQB1_2"]
    data = pd.read_pickle(input)
    data = data[data['loci']==5][["ID"]+loci_list]
    if drop_double:
        counter_dict = dict(data[loci_list].value_counts())
        data = data.drop_duplicates(subset=loci_list)
        name_d = "_no_d"
    arp_content_h_l, arp_content_fst = xl2arp(data)
    with open(f'output/output_h_l_{loci}{name_d}.arp', 'w') as arp_file:
        arp_file.write(arp_content_h_l)
    with open(f'output/output_amova_{loci}{name_d}.arp', 'w') as arp_file:
        arp_file.write(arp_content_fst)

elif loci in ['A','B','C','DRB1','DQB1']:
    loci_dict = {"A":["A1","A2"],"B":["B1","B2"],"C":["C1","C2"],"DRB1":["DRB1_1","DRB1_2"],"DQB1":["DQB1_1","DQB1_2"]}
    data = pd.read_pickle(input)[["ID"]+loci_dict[loci]]
    if drop_double:
        counter_dict = dict(data[loci_dict[loci]].value_counts())
        data = data.drop_duplicates(subset=loci_dict[loci])
        name_d = "_no_d"
    data = data.dropna()
    arp_content_h_l, arp_content_fst = xl2arp(data)
    with open(f'output/output_h_l_{loci}{name_d}.arp', 'w') as arp_file:
        arp_file.write(arp_content_h_l)
    with open(f'output/output_amova_{loci}{name_d}.arp', 'w') as arp_file:
        arp_file.write(arp_content_fst)
else:
    loci_list = ["A1","A2","B1","B2","C1","C2","DRB1_1","DRB1_2","DQB1_1","DQB1_2"]
    data = pd.read_pickle(input)[["ID"]+loci_list]
    data = data.fillna('?')
    if drop_double:
        counter_dict = dict(data[loci_list].value_counts())
        data = data.drop_duplicates(subset=loci_list)
        name_d = "_no_d"
    arp_content_h_l, arp_content_fst = xl2arp(data)
    with open(f'output/output_h_l{name_d}.arp', 'w') as arp_file:
        arp_file.write(arp_content_h_l)
    with open(f'output/output_amova{name_d}.arp', 'w') as arp_file:
        arp_file.write(arp_content_fst)

# python3 2.1.excel2arp.py -i all_original_unmerged.pickle -l 3 -d
