import pandas as pd


def xl2arp(data):
    # Initialize the ARP file content
    arp_content_fst = arp_content_h_l = f'''[Profile]

    Title="Genetic Data from Greek Populations"'''

    arp_content_fst += f'''
    NbSamples={len(data)}
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
SampleSize={len(data)}
SampleData= {{
'''

    counter = 0
    total = len(data)

    for index, row in data.iterrows():
        counter +=1
        if loci == 3:
            arp_content_h_l += f"{row['ID']}\t" + "1\t" + '\t'.join(row[['A1','B1','DRB1_1']]) + "\n" + "\t" + '\t'.join(row[['A2','B2','DRB1_2']]) + "\n"
            arp_content_fst += f'''SampleName="{row['ID']}"\nSampleSize=1\nSampleData= {{\n{row['ID']}\t''' + "1\t" + '\t'.join(row[['A1','B1','DRB1_1']]) + "\n" + "\t" + '\t'.join(row[['A2','B2','DRB1_2']]) + "}\n\n"
        elif loci in ['A','B','C','DRB1','DQB1']:
            arp_content_h_l += f"{row['ID']}\t" + "1\t" + '\t'.join(row[loci_dict[loci]]) + "\n"
            arp_content_fst += f'''SampleName="{row['ID']}"\nSampleSize=1\nSampleData= {{\n{row['ID']}\t''' + "1\t" + row[loci_dict[loci][0]] + "\n" + "\t" + row[loci_dict[loci][1]] + "}\n\n"
        else:
            arp_content_h_l += f"{row['ID']}\t" + "1\t" + '\t'.join(row[['A1','B1','C1','DRB1_1','DQB1_1']]) + "\n" + "\t" + '\t'.join(row[['A2','B2','C2','DRB1_2','DQB1_2']]) + "\n"
            arp_content_fst += f'''SampleName="{row['ID']}"\nSampleSize=1\nSampleData= {{\n{row['ID']}\t''' + "1\t" + '\t'.join(row[['A1','B1','C1','DRB1_1','DQB1_1']]) + "\n" + "\t" + '\t'.join(row[['A2','B2','C2','DRB1_2','DQB1_2']]) + "}\n\n"
        print(f"{counter}/{total}",end="\r")

    # Write the ARP file
    arp_content_h_l += "}\n\n"
    return arp_content_h_l, arp_content_fst
    

input = 'all_original_unmerged.pickle'
loci = 'A'

if loci == 3:
    data = pd.read_pickle(input)[["ID","A1","A2","B1","B2","DRB1_1","DRB1_2"]]
    arp_content_h_l, arp_content_fst = xl2arp(data)
    with open(f'output_h_l_{loci}.arp', 'w') as arp_file:
        arp_file.write(arp_content_h_l)
    with open(f'output_fst_{loci}.arp', 'w') as arp_file:
        arp_file.write(arp_content_fst)

elif loci == 5:
    data = pd.read_pickle(input)
    data = data[data['loci']==5][["ID","A1","A2","B1","B2","C1","C2","DRB1_1","DRB1_2","DQB1_1","DQB1_2"]]
    arp_content_h_l, arp_content_fst = xl2arp(data)
    with open(f'output_h_l_{loci}.arp', 'w') as arp_file:
        arp_file.write(arp_content_h_l)
    with open(f'output_fst_{loci}.arp', 'w') as arp_file:
        arp_file.write(arp_content_fst)

elif loci in ['A','B','C','DRB1','DQB1']:
    loci_dict = {"A":["A1","A2"],"B":["B1","B2"],"C":["C1","C2"],"DRB1":["DRB1_1","DRB1_2"],"DQB1":["DQB1_1","DQB1_2"]}
    data = pd.read_pickle(input)[["ID"]+loci_dict[loci]]
    data = data.dropna()
    arp_content_h_l, arp_content_fst = xl2arp(data)
    with open(f'output_h_l_{loci}.arp', 'w') as arp_file:
        arp_file.write(arp_content_h_l)
    with open(f'output_fst_{loci}.arp', 'w') as arp_file:
        arp_file.write(arp_content_fst)

else:
    data = pd.read_pickle(input)[["ID","A1","A2","B1","B2","C1","C2","DRB1_1","DRB1_2","DQB1_1","DQB1_2"]]
    data = data.fillna('?')
    arp_content_h_l, arp_content_fst = xl2arp(data)
    with open('output_h_l.arp', 'w') as arp_file:
        arp_file.write(arp_content_h_l)
    with open('output_fst.arp', 'w') as arp_file:
        arp_file.write(arp_content_fst)



#chmod +x arlecore3522_64bit
#bash arlecore_linux/LaunchArlecore.sh output.arp arlecore_linux/arl_run.ars