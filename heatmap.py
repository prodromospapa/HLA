import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import argparse

with open('ouput.npy', 'rb') as f:
    data = np.load(f)

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--id','-i', type=str, help='ID')

args = parser.parse_args()

id_list = pd.read_pickle("all_np.pickle")["ID"].tolist()# find a better way to load ids
counter = 0
for id in id_list:
    counter+=1
    df_data = pd.DataFrame(data[id_list.index(id)])
    cmap_dict = {-1: "white", 0: 'black', 1: 'yellow', 2: 'red'}
    cmap = ListedColormap([cmap_dict[i] for i in cmap_dict.keys()])
    sns.heatmap(df_data,xticklabels=["A", "B", "C", "DRB1", "DQB1"],yticklabels=[],cmap=cmap)
    plt.title(id)
    plt.savefig(f'heatmaps/{id}.png', dpi=300)
    plt.close()
    print(f"{counter}/{len(id_list)}", end="\r")