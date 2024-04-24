import pandas as pd


def xl2arp(data, output_path):
    # Initialize the ARP file content
    arp_content = f"""[Profile]

    Title="Genetic Data from Greek Populations"
    NbSamples={len(data)}
    GenotypicData=1
    GameticPhase=0
    DataType=STANDARD 
    LocusSeparator=TAB 
    RecessiveData=0
    MissingData='?'

[Data]

[[Samples]]

"""

    arp_content += f'''SampleName="Greece"
SampleSize={len(data)}
SampleData= {{
'''
    counter = 0
    total = len(data)
    for index, row in data.iterrows():
        counter +=1
        arp_content += f"{row['ID']}\t" + "1\t" + '\t'.join(row[['A1','B1','C1','DRB1_1','DQB1_1']]) + "\n" + "\t" + '\t'.join(row[['A2','B2','C2','DRB1_2','DQB1_2']]) + "\n"
        print(f"{counter}/{total}",end="\r")

    # Write the ARP file
    arp_content += "}\n\n"
    with open(output_path, 'w') as arp_file:
        arp_file.write(arp_content)


data = pd.read_pickle('all_original_unmerged.pickle')[["ID","A1","A2","B1","B2","C1","C2","DRB1_1","DRB1_2","DQB1_1","DQB1_2"]].iloc[0:100]
data = data.fillna('?')

# Call the xl2arp function with the loci, grouped alleles, data paths, and output path
xl2arp(data, 'output.arp')