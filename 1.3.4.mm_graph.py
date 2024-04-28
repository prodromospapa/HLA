import pandas as pd
import argparse
import matplotlib.pyplot as plt
import os

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--choose','-c', choices=['BMD','CBU','all'],type=str, help='Direction(GvH or HvG)', required=True)
parser.add_argument('--direction','-d', choices=['GvH','HvG'], help='Direction(GvH or HvG)', required=True)
parser.add_argument('--type','-t', choices=['allele','genotype'], help='Type of data to be saved', required=True)

args = parser.parse_args()

mm_per_df = pd.read_pickle(f"{args.choose}_{args.direction}_{args.type}_mm_per.pickle")
al_per_df = pd.read_pickle(f"{args.choose}_{args.direction}_{args.type}_freq_per.pickle")

# Create 'plots' folder if it doesn't exist
if not os.path.exists('plots'):
        os.makedirs('plots')

for base in ["A","B","C","DRB1","DQB1"]:
    mm_per = mm_per_df[base].dropna()
    al_per = al_per_df[base].reindex(mm_per.index).sort_values(ascending=False)
    mm_per = mm_per.reindex(al_per.index)
    for mm,color in enumerate(["blue","red","green"]):
        mm_list = [allele[mm] for allele in mm_per]
        plt.plot(mm_list,color=color)
    plt.bar(mm_per.index,al_per.tolist(),color="black",alpha=0.5)
    plt.legend(["0","1","2","Allele Frequency"])
    plt.rcParams['xtick.labelsize'] = 6
    plt.xticks(range(len(mm_per)),mm_per.index,rotation=90,fontsize=1)
    plt.title(f"{args.choose}_{args.direction}_{base}")
    plt.tight_layout()
    plt.savefig(f"plots/{args.choose}_{args.direction}_{base}_{args.type}_sorted.png",dpi=1000)
    plt.close()

#python3 1.3.4.mm_graph.py -c CBU -d HvG