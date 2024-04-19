import pandas as pd
import argparse
from statistics import mean
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--choose','-c', choices=['BMD','CBU','all'],type=str, help='Direction(GvH or HvG)', required=True)
parser.add_argument('--direction','-d', choices=['GvH','HvG'], help='Direction(GvH or HvG)', required=True)

args = parser.parse_args()

mm_per_df = pd.read_pickle(f"{args.choose}_{args.direction}_mm_per.pickle")
al_per_df = pd.read_pickle(f"{args.choose}_{args.direction}_al_per.pickle")

mm_per = mm_per_df
al_per = al_per_df.reindex(mm_per.index)

plot = True
for ranking in [[1,0.1],[0.1,0.05],[0.05,0]]:
        ranking_values_list = [y for x in mm_per[al_per<ranking[0]][al_per >=ranking[1]].values.tolist() for y in x if type(y).__name__=="dict"]
        zeros = [dictionary[0] for dictionary in ranking_values_list]
        ones = [dictionary[1] for dictionary in ranking_values_list]
        twos = [dictionary[2] for dictionary in ranking_values_list]
        if plot:
                plt.plot(sorted(zeros),color="blue")
                plt.plot(sorted(ones),color="red")
                plt.plot(sorted(twos),color="green")
                plt.legend(["0","1","2"])
                plt.title(f"{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}")
                plt.tight_layout()
                plt.savefig(f"{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}.png",dpi=300)
                plt.close()
        else:
                print(f"{ranking}: zeros: {zeros}, ones: {ones}, twos: {twos}")


#python3 helen_ranking.py -c CBU -d HvG