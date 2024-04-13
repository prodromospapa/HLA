import dask.dataframe as dd #conda install -c conda-forge s3fs
import argparse
import pandas as pd

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--id','-i', type=str, help='',required=False)
parser.add_argument('--number','-n', type=str, help='',required=False)

args = parser.parse_args()

df = pd.read_pickle('all_np.pickle')
data = dd.from_pandas(df, npartitions=1)
if args.id:
    if "," not in args.id:
        id = [args.id]  # loci are passed as command line arguments, ["A","B", "C", "DRB1", "DQB1", "DPB1"]
    else:
        id = args.id.split(",")
        id = [i.strip() for i in id]
        
    print(data.loc[id].head(len(id)))

elif args.number:
    if "," not in args.number:
        n = [int(args.number)]  # loci are passed as command line arguments, ["A","B", "C", "DRB1", "DQB1", "DPB1"]
    else:
        n = args.number.split(",")
        n = [int(i.strip()) for i in n]
    print(data.loc[df.index[n]].head(len(n)))

# python3 genotype_finder.py -i "CBMDP-0000511,CBMDP-0000512"
# python3 genotype_finder.py -n '10,11'