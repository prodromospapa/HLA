import pandas as pd


def xl2arp(data):
    # Initialize the ARP file content
    arp_content_fst = arp_content_h_l = f"""[Profile]

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

    arp_content_h_l += f'''SampleName="Greece"
SampleSize={len(data)}
SampleData= {{
'''

    counter = 0
    total = len(data)

    for index, row in data.iterrows():
        counter +=1
        arp_content_h_l += f"{row['ID']}\t" + "1\t" + '\t'.join(row[['A1','B1','C1','DRB1_1','DQB1_1']]) + "\n" + "\t" + '\t'.join(row[['A2','B2','C2','DRB1_2','DQB1_2']]) + "\n"
        arp_content_fst += f'''SampleName={row['ID']}\nSampleSize=1\nSampleData= {{\n{row['ID']}\t''' + "1\t" + '\t'.join(row[['A1','B1','C1','DRB1_1','DQB1_1']]) + "\n" + "\t" + '\t'.join(row[['A2','B2','C2','DRB1_2','DQB1_2']]) + "}\n"
        print(f"{counter}/{total}",end="\r")

    # Write the ARP file
    arp_content_h_l += "}\n\n"
    arp_content_fst += "}\n\n"
    with open('output_h_l.arp', 'w') as arp_file:
        arp_file.write(arp_content_h_l)
    with open('output_fst.arp', 'w') as arp_file:
        arp_file.write(arp_content_fst)



data = pd.read_pickle('all_original_unmerged.pickle')[["ID","A1","A2","B1","B2","C1","C2","DRB1_1","DRB1_2","DQB1_1","DQB1_2"]]
data = data.fillna('?')

# Call the xl2arp function with the loci, grouped alleles, data paths, and output path
xl2arp(data)

#chmod +x arlecore3522_64bit
#bash arlecore_linux/LaunchArlecore.sh output.arp arlecore_linux/arl_run.ars