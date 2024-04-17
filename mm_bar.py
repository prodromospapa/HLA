import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse
from statistics import mean

def bar(choose,loci,direction):
    with open(f'{choose}_{direction}.npy', 'rb') as f:
        data = np.load(f,allow_pickle=True)

    all = pd.read_pickle("all.pickle")
    if choose in ['BMD','CBU']:
        all = all[all['source']== choose].reset_index(drop=True)
    id = all["ID"].tolist()
    loci_dict = {"A":0,"B":1,"C":2,"DRB1":3,"DQB1":4,'3':1,'5': 2}
    y1_total = []
    y2_total = []
    y3_total = []
    for i,x in enumerate(id):
        if choose in ['3','5']:
            row = data[i][loci_dict[loci]]
        else:
            row = data[i][0][loci_dict[loci]]
        if row != None:
            y1 = row[0]
            y1_total.append(y1)
            plt.bar(x,y1,color='b')
            
            y2 = row[1]
            y2_total.append(y2)
            plt.bar(x,y2,bottom=y1,color='r')

            y3 = row[2]
            y3_total.append(y3)
            plt.bar(x,y3,bottom=y1+y2,color='g')    
        print(f"{i+1}/{len(id)}",end="\r")
    plt.axhline(mean(y1_total), color='blue')
    plt.axhline(mean(y2_total), color='red')
    plt.axhline(mean(y3_total), color='green')
    plt.title(f"{choose}_{direction}_{loci}")
    plt.savefig(f"{choose}_{direction}_{loci}.png")

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--choose','-c', choices=['BMD','CBU','all'],type=str, help='Sample origin', required=True)
parser.add_argument('--loci','-l', choices=["A","B","C","DRB1","DQB1",'3','5'],type=str, help='Loci', required=True)
parser.add_argument('--direction','-d', choices=['GvH','HvG'], help='Direction(GvH or HvG)', required=True)

args = parser.parse_args()

bar(args.choose,args.loci,args.direction)