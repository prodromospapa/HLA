import pandas as pd
import argparse
import os


def xl2arp(data):
    banks = data['bank'].unique()
    # Initialize the ARP file content
    if args.total:
        nbsample = 1
    else:
        nbsample = len(banks)

    arp_content = f'''[Profile]

    Title="Genetic Data"
    NbSamples={nbsample}
    GenotypicData=1'''
    
    if args.database == "Greece":
        arp_content += "\n    GameticPhase=0\n"
    else:
        arp_content += "\n    GameticPhase=1\n"

    arp_content += '''    DataType=STANDARD 
    LocusSeparator=TAB 
    RecessiveData=0
    MissingData='?'

[Data]

[[Samples]]
'''
    counter = 0
    total = len(data)
    if args.database == "Greece" and loci == '3':
        loci_l = [['A1','B1','DRB1_1'],['A2','B2','DRB1_2']]
    else:
        loci_l = [['A1','B1','C1','DRB1_1','DQB1_1'],['A2','B2','C2','DRB1_2','DQB1_2']]
    if args.total:
        arp_content += f'''SampleName="{args.database}"
    SampleSize={len(data)}
    SampleData= {{
'''
        for index, row in data.iterrows():
            counter +=1
            if args.database == "Greece":
                id = row['ID']
            else:
                id = row['bank']+ "_" +str(counter)
            arp_content += f"{id}\t" + f"1\t" + '\t'.join(row[loci_l[0]]) + "\n" + "\t" + '\t'.join(row[loci_l[1]]) + "\n"
            print(f"{counter}/{total}",end="\r")
        arp_content += "}\n\n"
        if args.database == "DKMS":
            arp_content += f'''[[Structure]]
    StructureName="Simulated data"
    NbGroups=1
    Group={{
    "DKMS"
    }}'''
    else:
        for bank in banks:
            data_loop = data[data['bank']==bank]
            arp_content += f'''SampleName="{bank}"
    SampleSize={len(data_loop)}
    SampleData= {{
    '''
            for index, row in data_loop.iterrows():
                counter +=1
                if args.database == "Greece":
                    id = row['ID']
                else:
                    id = row['bank']+ "_" +str(counter)
                arp_content += f"{id}\t" + f"1\t" + '\t'.join(row[loci_l[0]]) + "\n" + "\t" + '\t'.join(row[loci_l[1]]) + "\n"
                print(f"{counter}/{total}",end="\r")
            arp_content += "}\n\n"
        if args.database == "DKMS":
            arp_content += f'''[[Structure]]
    StructureName="Simulated data"
    NbGroups=1
    Group={{
    '''
        for bank in banks:
            arp_content+=f'    "{bank}"\n'
        arp_content += '}'
    return arp_content
    
parser = argparse.ArgumentParser(description='Convert excel file to arlequin format')
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
    loci = args.loci
    input = "all_original_unmerged.pickle"

    # Create the output folder if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')

    data = pd.read_pickle(input)

    if loci == '3':
        loci_list = ["A1","A2","B1","B2","DRB1_1","DRB1_2"]
        data = data[["ID","bank"]+loci_list]
        arp_content= xl2arp(data)
        with open(f'output/output_{loci}{total}.arp', 'w') as arp_file:
            arp_file.write(arp_content)

    elif loci == '5':
        loci_list = ["A1","A2","B1","B2","C1","C2","DRB1_1","DRB1_2","DQB1_1","DQB1_2"]
        data = data[data['loci']==5][["ID","bank"]+loci_list]
        arp_content= xl2arp(data)
        with open(f'output/output_{loci}{total}.arp', 'w') as arp_file:
            arp_file.write(arp_content)

    os.system(f'bash arlecore_linux/LaunchArlecore.sh output/output_{loci}{total}.arp ELB')
    os.system(f"mv output/output_{loci}{total}.res/PhaseDistribution/ELB_Best_Phases.arp output/output_{loci}{total}.arp")
    os.system(f"rm -r output/output_{loci}{total}.res/PhaseDistribution/")
else:
    data = pd.read_pickle("dkms.pkl")
    data = data[["bank","A1","A2","B1","B2","C1","C2","DRB1_1","DRB1_2","DQB1_1","DQB1_2"]]
    arp_content= xl2arp(data)
    with open(f'output/output_dkms{total}.arp', 'w') as arp_file:
        arp_file.write(arp_content)

    