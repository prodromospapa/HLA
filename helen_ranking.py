import pandas as pd
import argparse
from statistics import mean

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

for ranking in [[1,0.1],[0.1,0.05],[0.05,0]]:
        ranking_values_list = [y for x in mm_per[al_per<ranking[0]][al_per >=ranking[1]].values.tolist() for y in x if type(y).__name__=="dict"]
        zeros = mean([dictionary[0] for dictionary in ranking_values_list])
        ones = mean([dictionary[1] for dictionary in ranking_values_list])
        twos = mean([dictionary[2] for dictionary in ranking_values_list])
        print(f"{ranking}: zeros: {zeros}, ones: {ones}, twos: {twos}")


#python3 helen_ranking.py -c CBU -d HvG