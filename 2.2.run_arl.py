import argparse
import os

def permutation_type(x):
    x = int(x)
    if x < 1:
        raise argparse.ArgumentTypeError("Minimum permutation value is 1")
    return x


parser = argparse.ArgumentParser(description='ARP file generator')
parser.add_argument('--database','-d', type=str,choices=["Greece","DKMS"], help='database to use', required=True)
parser.add_argument('--loci','-l', type=str,choices=['3','5'], help='Number of loci',required='-d'=="Greece")
parser.add_argument('--total','-to', action='store_true', help='Total of database', required=False)
parser.add_argument("--type",'-t', type=str,choices=['CBU','BMD',"all"], help='Type of data', required="-to"==True)

args = parser.parse_args()

if args.total:
    total = "_total"
else:
    total = ""

if args.type == "CBU":
    type_ = "_CBU"
elif args.type == "BMD":
    type_ = "_BMD"
else:
    type_ = ""

if args.database == "Greece":
    input_text = f"output/output_{args.loci}{total}{type_}.arp"
else:
    input_text = f"output/output_dkms{total}.arp"


#os.system(f"bash arlecore_linux/LaunchArlecore.sh {input_text} POP") # afto einai phased
os.system(f"bash arlecore_linux/LaunchArlecore.sh {input_text} STATS")

# python3 2.2.run_arl.py -t HL -p 10 -l 3
#chmod +x arlecore_linux/arlecore3522_64bit