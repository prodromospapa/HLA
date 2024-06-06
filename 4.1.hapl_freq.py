import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--loci','-l', type=str,choices=['3','5'], help='Number of loci',required=True)

args = parser.parse_args()

if not os.path.exists('bootstrap'):
    os.makedirs('bootstrap')
    

data = pd.read_pickle("all_original_unmerged.pickle")
if args.loci == '5':
    data = data[data["loci"]==5]
all_ids = data["ID"].tolist()
data = data[data["type"]=="CBU"] 
ids = data["ID"].tolist()

remove_ids = [i for i in all_ids if i not in ids]
with open("remove_ids.txt","w") as f:
    f.write("\n".join(remove_ids))
input_file = f"output_elb/output_{args.loci}_total.arp"
output_file = f"bootstrap/bootstrap_{args.loci}.arp"
os.system('''awk 'NR==FNR{a[$0];next} {if ($1 in a) {getline;next} else {print}}' remove_ids.txt ''' + f'"{input_file}" > "{output_file}"')
os.system(f"sed -i 's/SampleSize=[0-9]*/SampleSize={len(data)}/' {output_file}")

os.remove("remove_ids.txt")
input_text = f"bootstrap/bootstrap_{args.loci}.arp"
os.system(f"bash arlecore_linux/LaunchArlecore.sh {input_text} FREQ")


