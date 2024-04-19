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
parser.add_argument('--plot','-p', choices=['True','False'], help='', required=True)
parser.add_argument('--ranking','-r', help='Direction(GvH or HvG)', required=True,type=str)

args = parser.parse_args()

mm_per_df = pd.read_pickle(f"{args.choose}_{args.direction}_mm_per.pickle")
al_per_df = pd.read_pickle(f"{args.choose}_{args.direction}_al_per.pickle")

mm_per = mm_per_df
al_per = al_per_df.reindex(mm_per.index)


def ranking_plot(plot,ranking):
        for ranking in ranking:
                ranking_values_list = [[x[0]+"_"+base.name,x[1]] for index,base in mm_per[al_per<ranking[0]][al_per >=ranking[1]].iterrows() if base.dropna().values.all() for x in base.dropna().items()]
                zeros = sorted([[sample[0],sample[1][0]] for sample in ranking_values_list],key=lambda x: x[1])
                ones = sorted([[sample[0],sample[1][1]] for sample in ranking_values_list],key=lambda x: x[1])
                twos = sorted([[sample[0],sample[1][2]] for sample in ranking_values_list],key=lambda x: x[1])
                if plot:
                        plt.plot([x[0] for x in zeros],[x[1] for x in zeros],color="blue")
                        plt.title(f"{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}_zeros")
                        plt.xticks(rotation=90)
                        plt.tight_layout()
                        plt.savefig(f"{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}_zeros.png",dpi=300)
                        plt.close()
                        
                        plt.plot([x[0] for x in ones],[x[1] for x in ones],color="red")
                        plt.title(f"{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}_ones")
                        plt.xticks(rotation=90)
                        plt.tight_layout()
                        plt.savefig(f"{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}_ones.png",dpi=300)
                        plt.close()

                        plt.plot([x[0] for x in twos],[x[1] for x in twos],color="green")
                        plt.title(f"{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}_twos")
                        plt.xticks(rotation=90)
                        plt.tight_layout()
                        plt.savefig(f"{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}_twos.png",dpi=300)
                        plt.close()
                else:
                        print(f"{ranking}: zeros: {mean([x[1] for x in zeros])}, ones: {mean([x[1] for x in ones])}, twos: {mean([x[1] for x in twos])}")

ranking_plot(args.plot,eval(args.ranking))

#python3 helen_ranking_alleles.py -c CBU -d HvG -p True -r [[1,0.1],[0.1,0.05]]