import argparse
import os

def permutation_type(x):
    x = int(x)
    if x < 1:
        raise argparse.ArgumentTypeError("Minimum permutation value is 1")
    return x


parser = argparse.ArgumentParser(description='ARP file generator')
parser.add_argument('--test','-t', choices=["AMOVA","HL"] ,type=str, help='Type of test',required=True)
parser.add_argument('--permutation','-p', type=permutation_type, help='Number of permutations',required=True)
parser.add_argument('--loci','-l', type=str,choices=['3','5','A','B','C','DRB1','DQB1','all'], help='Number of loci',required=True)
parser.add_argument('--drop_double','-d', action='store_true', help='Drop double entries')

args = parser.parse_args()
if args.drop_double:
    add = "_no_d"
else:
    add = ""

if args.test == "HL":
    input_text = f"output/output_h_l_{args.loci}{add}.arp {args.permutation} {args.test}"
    if os.path.exists(f"output/output_h_l_{args.loci}{add}"):
        os.rmdir(f"output/output_h_l_{args.loci}{add}")
elif args.test == "AMOVA":
    input_text = f"output/output_amova_{args.loci}{add}.arp {args.permutation} {args.test}"
    if os.path.exists(f"output/output_amova_{args.loci}{add}"):
        os.rmdir(f"output/output_amova_{args.loci}{add}")

os.system(f"bash arlecore_linux/LaunchArlecore.sh {input_text}")

# python3 2.2.run_arl.py -t HL -p 10 -l 3 -d
#chmod +x arlecore_linux/arlecore3522_64bit