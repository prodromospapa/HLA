import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import argparse
import os

def bootstrap(data,size):
    boot = data.sample(n=size,replace=True)
    return boot

def bootstrap_phase(data,size):
    b1 = data[h1].sample(n=size,replace=True)
    b1.reset_index(drop=True,inplace=True)
    b2 = data[h2].sample(n=size,replace=True)
    b2.reset_index(drop=True,inplace=True)
    return pd.concat([b1,b2],axis=1)

def sort_row_pairs(row, pairs):
    sorted_values = []
    for col1, col2 in locus_list:
        sorted_pair = sorted([row[col1], row[col2]])
        sorted_values.extend(sorted_pair)
    return pd.Series(sorted_values, index=[col for pair in pairs for col in pair])

def format_df(df):
    sorted_df = df.apply(sort_row_pairs, pairs=locus_list, axis=1)
    return sorted_df

def counter_9(df):
    a = df[["A1", "A2", "B1", "B2", "C1", "C2", "DRB1_1", "DRB1_2", "DQB1_1"]].apply(lambda row: ' '.join(row.astype(str)), axis=1).value_counts()
    b = df[["A1", "A2", "B1", "B2", "C1", "C2", "DRB1_1", "DRB1_2", "DQB1_2"]].apply(lambda row: ' '.join(row.astype(str)), axis=1).value_counts()
    return a.add(b, fill_value=0)


def compare_6(recipient,size,n,pro,counter):
    results = []
    for _ in range(args.repeticions):
        if phase:
            donor_boot = bootstrap_phase(donor,size)
        else:
            donor_boot = bootstrap(donor,size)
        donor_boot = format_df(donor_boot)
        donor_boot_counts = donor_boot.apply(lambda row: ' '.join(row.astype(str)), axis=1).value_counts()
        v = recipient.apply(lambda row: ' '.join(row.astype(str)), axis=1).map(donor_boot_counts).dropna().astype(np.int8)
        results.append(len(v)/total_recipient)
        if n == 0:
            counter += 1
            print(f"{counter}/{pro}",end="\r")
    return results,counter

def compare_9_10(recipient,size,n,pro,counter):
    ni = []
    te = []
    for _ in range(args.repeticions):
        if phase:
            donor_boot = bootstrap_phase(donor,size)
        else:
            donor_boot = bootstrap(donor,size)
        donor_boot = format_df(donor_boot)
        donor_boot_counts_9 = counter_9(donor_boot)
        a = recipient[["A1", "A2", "B1", "B2", "C1", "C2", "DRB1_1", "DRB1_2", "DQB1_1"]].apply(lambda row: ' '.join(row.astype(str)), axis=1).map(donor_boot_counts_9).dropna().astype(np.int8)
        b = recipient[["A1", "A2", "B1", "B2", "C1", "C2", "DRB1_1", "DRB1_2", "DQB1_2"]].apply(lambda row: ' '.join(row.astype(str)), axis=1).map(donor_boot_counts_9).dropna().astype(np.int8)
        nines = list(set(a.index) - set(b.index))
        tens = list(set(a.index) & set(b.index))
        ni.append(len(nines)/total_recipient)
        te.append(len(tens)/total_recipient)
        if n == 0:
            counter += 1
            print(f"{counter}/{pro}",end="\r")
    return ni,te,counter

def matches(part):
    n = part[0]
    sizes = part[1]
    meann = {}
    maxx = {}
    minn = {}
    meann_9 = {}
    maxx_9 = {}
    minn_9 = {}
    counter = 0
    pro = len(sizes)*args.repeticions
    for size in sizes:
        if size:
            if loci== 3:                
                res,counter = compare_6(recipient,size,n,pro,counter)
                meann[size] = np.mean(res)
                maxx[size] = np.max(res)
                minn[size] = np.min(res)
            else:

                ni,te,counter = compare_9_10(recipient,size,n,pro,counter)
                meann[size] = np.mean(ni)
                meann_9[size] = np.mean(te)
                maxx[size] = np.max(ni)
                maxx_9[size] = np.max(te)
                minn[size] = np.min(ni)
                minn_9[size] = np.min(te)
    if loci == 3:
        return meann,minn,maxx
    else:
        return meann,minn,maxx,meann_9,minn_9,maxx_9

def split_and_transpose(lst, n):
    sublists = [lst[i:i + n] for i in range(0, len(lst), n)]
    max_len = max(len(sublist) for sublist in sublists)
    sublists = [sublist + [False] * (max_len - len(sublist)) for sublist in sublists]
    return list(map(list, zip(*sublists)))

def run(n):
    sizes = list(range(min_size, max_size + 1,step))
    size_list = split_and_transpose(sizes, n)
    size_list = sorted(size_list,key=sum,reverse=True)
    partitions = list(zip(range(n),size_list))
    p = Pool(processes=n)
    if loci == 3:
        meann,minn,maxx = zip(*p.map(matches, partitions))
        p.close()
    else:
        meann,minn,maxx,meann_9,minn_9,maxx_9 = zip(*p.map(matches, partitions))
        p.close()
        meann_9 = {k: v for d in meann_9 for k, v in d.items()}
        meann_9 = dict(sorted(meann_9.items()))
        maxx_9 = {k: v for d in maxx_9 for k, v in d.items()}
        maxx_9 = dict(sorted(maxx_9.items()))
        minn_9 = {k: v for d in minn_9 for k, v in d.items()}
        minn_9 = dict(sorted(minn_9.items()))
    meann = {k: v for d in meann for k, v in d.items()}
    meann = dict(sorted(meann.items()))
    maxx = {k: v for d in maxx for k, v in d.items()}
    maxx = dict(sorted(maxx.items()))
    minn = {k: v for d in minn for k, v in d.items()}
    minn = dict(sorted(minn.items()))
    if loci == 3:
        return meann,minn,maxx
    else:
        return meann,minn,maxx,meann_9,minn_9,maxx_9

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--threads','-t', type=int, help='Number of threads to use', required=True)
parser.add_argument('--phase','-p', action='store_true', help='Phase the data')
parser.add_argument('--loci','-l', type=int, help='Number of loci to use', required=True)
parser.add_argument('--size','-s', type=int, help='Size of the bootstraps', required=True)
parser.add_argument('--sampling','-sam', type=float, help='Sampling rate', required=True)
parser.add_argument('--donor','-d', type=str,choices=["all","CRETE","PAP","CBMDP","BRFAA"],help='Donor bank', required=True)
parser.add_argument('--recipient','-r', type=str,choices=["all","CRETE","PAP","CBMDP","BRFAA"],help='Recipient bank', required=True)
parser.add_argument('--repeticions','-rep', type=int, help='Number of repeticions', required=True)


args = parser.parse_args()

loci = args.loci
phase = args.phase
min_size = 1
max_size = args.size
step = int((max_size-min_size)*args.sampling)
total = pd.read_pickle(f"data/phased_{loci}.pkl")

if loci == 5:
    table = total[["bank","type","A1", "A2", "B1", "B2", "C1", "C2", "DRB1_1", "DRB1_2", "DQB1_1", "DQB1_2"]]
    h1 = ["A1", "B1", "C1", "DRB1_1", "DQB1_1"]
    h2 = ["A2", "B2", "C2", "DRB1_2", "DQB1_2"]
    locus_list = [["A1","A2"],["B1","B2"],["C1","C2"],["DRB1_1","DRB1_2"],["DQB1_1","DQB1_2"]]
elif loci == 3:
    table = total[["bank","type","A1", "A2", "B1", "B2", "DRB1_1", "DRB1_2"]]
    h1 = ["A1", "B1", "DRB1_1"]
    h2 = ["A2", "B2", "DRB1_2"]
    locus_list = [["A1","A2"],["B1","B2"],["DRB1_1","DRB1_2"]]


#pick donors pool
donor = table
if args.donor != "all":
    donor = table[table["bank"] == args.donor]
donor = donor.drop(columns="bank")
donor = table[table["type"] == "CBU"]
donor = donor.drop(columns="type")

#pick recipients
recipient = table
if args.recipient != "all":
    recipient = table[table["bank"] == args.recipient]
recipient= recipient.drop(columns="bank")
recipient = recipient.drop(columns="type")
recipient = format_df(recipient)
total_recipient = len(recipient)
if loci == 3:
    meann,minn,maxx = run(args.threads)
else:
    meann,minn,maxx,meann_9,minn_9,maxx_9 = run(args.threads)

plt.plot(meann.keys(),np.array(list(meann.values()))*100,label="all",color="blue")
plt.fill_between(meann.keys(),np.array(list(minn.values()))*100,np.array(list(maxx.values()))*100,alpha=0.5,color="blue")
if loci == 5:
    plt.plot(meann_9.keys(),np.array(list(meann_9.values()))*100,label="9/10",color="red")
    plt.fill_between(meann_9.keys(),np.array(list(minn_9.values()))*100,np.array(list(maxx_9.values()))*100,alpha=0.5,color="red")
plt.legend()
plt.xlabel("Number of Donors")
plt.ylabel("Percentage of matches (%)")
if not os.path.isdir("size_plots"):
    os.mkdir("size_plots")
if phase:
    plt.title(f"Bootstrap analysis of {loci} loci Phased")
    plt.savefig(f"size_plots/size_{loci}_phased.png")
else:
    plt.title(f"Bootstrap analysis of {loci} loci")
    plt.savefig(f"size_plots/size_{loci}.png")
