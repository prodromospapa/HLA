import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import argparse
import os

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--id','-i', type=str, help='ID')

args = parser.parse_args()
id_list = pd.read_pickle("all_np.pickle").index.tolist()# find a better way to load ids

directions = ["GvH", "HvG"]
for direction in directions:
    plt.subplot(1, 2, directions.index(direction)+1)
    f = open(f'ouput_{direction}.npy', 'rb')
    data = np.load(f)
    df_data = pd.DataFrame(data[id_list.index(args.id)])
    cmap_dict = {-1: "white", 0: 'black', 1: 'yellow', 2: 'red'}
    cmap = ListedColormap([cmap_dict[i] for i in cmap_dict.keys()])
    sns.heatmap(df_data,xticklabels=["A", "B", "C", "DRB1", "DQB1"],yticklabels=[],cmap=cmap)
    plt.title(f"{args.id} ({direction})")
    f.close()
plt.tight_layout()    
#plt.savefig(f'{args.id}.png', dpi=300)
plt.show()