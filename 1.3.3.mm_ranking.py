import pandas as pd
import argparse
from statistics import mean
import os
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--choose','-c', choices=['BMD','CBU','all'],type=str, help='Direction(GvH or HvG)', required=True)
parser.add_argument('--direction','-d', choices=['GvH','HvG'], help='Direction(GvH or HvG)', required=True)
parser.add_argument('--plot','-p', action='store_true', help='Return plot')
parser.add_argument('--ranking','-r', help='Dictionary with ranking (e.g. [[1,0.1],[0.1,0.05]])', required=True,type=str)
parser.add_argument('--sort','-s', choices=['value','name'], help='Sort by value or name')

args = parser.parse_args()

mm_per_df = pd.read_pickle(f"{args.choose}_{args.direction}_mm_per.pickle")
al_per_df = pd.read_pickle(f"{args.choose}_{args.direction}_al_per.pickle")

mm_per = mm_per_df
al_per = al_per_df.reindex(mm_per.index)

# Create 'plots' folder if it doesn't exist
if not os.path.exists('plots'):
        os.makedirs('plots')

def ranking_plot(plot,ranking_list,sort):
        for ranking in ranking_list:
                #alleles
                ranking_values_list = [[x[0]+"_"+base.name,x[1]] for index,base in mm_per[al_per<ranking[0]][al_per >=ranking[1]].iterrows() if base.dropna().values.all() for x in base.dropna().items()]
                sort_way = 0 if sort == "name" else 1
                zeros = sorted([[sample[0],sample[1][0]] for sample in ranking_values_list],key=lambda x: x[sort_way])
                ones = sorted([[sample[0],sample[1][1]] for sample in ranking_values_list],key=lambda x: x[sort_way])
                twos = sorted([[sample[0],sample[1][2]] for sample in ranking_values_list],key=lambda x: x[sort_way])
                #total
                ranking_values_list_total = [y for x in mm_per[al_per<ranking[0]][al_per >=ranking[1]].values.tolist() for y in x if type(y).__name__=="dict"]
                zeros_total = [dictionary[0] for dictionary in ranking_values_list_total]
                ones_total = [dictionary[1] for dictionary in ranking_values_list_total]
                twos_total = [dictionary[2] for dictionary in ranking_values_list_total]
                if plot:
                        if sort_way == 0:
                                plt.plot([x[0] for x in zeros],[x[1] for x in zeros],color="blue")
                                plt.plot([x[0] for x in ones],[x[1] for x in ones],color="red")
                                plt.plot([x[0] for x in twos],[x[1] for x in twos],color="green")
                                plt.title(f"{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}_sortbyname")
                                plt.xticks(rotation=90)
                                plt.legend(["0","1","2"])
                                plt.tight_layout()
                                plt.savefig(f"plots/{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}_sortbyname.png",dpi=300)
                                plt.close()
                        else:
                                plt.plot([x[0] for x in zeros],[x[1] for x in zeros],color="blue")
                                plt.title(f"{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}_zeros_sortbyvalue")
                                plt.xticks(rotation=90)
                                plt.tight_layout()
                                plt.savefig(f"plots/{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}_zeros_sortbyvalue.png",dpi=300)
                                plt.close()
                                
                                plt.plot([x[0] for x in ones],[x[1] for x in ones],color="red")
                                plt.title(f"{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}_ones_sortbyvalue")
                                plt.xticks(rotation=90)
                                plt.tight_layout()
                                plt.savefig(f"plots/{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}_ones_sortbyvalue.png",dpi=300)
                                plt.close()

                                plt.plot([x[0] for x in twos],[x[1] for x in twos],color="green")
                                plt.title(f"{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}_twos_sortbyvalue")
                                plt.xticks(rotation=90)
                                plt.tight_layout()
                                plt.savefig(f"plots/{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}_twos_sortbyvalue.png",dpi=300)
                                plt.close()
                        #plot total
                        plt.plot(sorted(zeros_total),color="blue")
                        plt.plot(sorted(ones_total),color="red")
                        plt.plot(sorted(twos_total),color="green")
                        plt.legend(["0","1","2"])
                        plt.title(f"{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}")
                        plt.tight_layout()
                        plt.savefig(f"plots/{args.choose}_{args.direction}_ranking_{ranking[0]}_{ranking[1]}_total.png",dpi=300)
                        plt.close()
                else:
                        print(f"{ranking}: zeros: {mean([x[1] for x in zeros])}, ones: {mean([x[1] for x in ones])}, twos: {mean([x[1] for x in twos])}")

ranking_plot(args.plot,eval(args.ranking),args.sort)

#python3 helen_ranking_alleles.py -c CBU -d HvG -p -s value -r [[1,0.1],[0.1,0.05],[0.05,0.01],[0.01,0.001],[0.001,0]]
#python3 helen_ranking_alleles.py -c CBU -d HvG -p -s name -r [[1,0.1],[0.1,0.05],[0.05,0.01],[0.01,0.001],[0.001,0]]

#python3 helen_ranking_alleles.py -c CBU -d HvG -r [[1,0.1],[0.1,0.05],[0.05,0.01],[0.01,0.001],[0.001,0]]
#python3 helen_ranking_alleles.py -c CBU -d HvG -r [[1,0.1],[0.1,0.05],[0.05,0.01],[0.01,0.001],[0.001,0]]