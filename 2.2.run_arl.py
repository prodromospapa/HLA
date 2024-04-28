import argparse
import os

parser = argparse.ArgumentParser(description='ARP file generator')
parser.add_argument('--test','-t', choices=["AMOVA","HL"] ,type=str, help='Type of test',required=True)
parser.add_argument('--permutation','-p', type=int, help='Number of permutations',required=True)
parser.add_argument('--loci','-l', type=str,choices=['3','5','A','B','C','DRB1','DQB1','all'], help='Number of loci',required=True)
parser.add_argument('--drop_double','-d', action='store_true', help='Drop double entries')

args = parser.parse_args()
if args.drop_double:
    add = "_no_d"
else:
    add = ""

if args.test == "HL":
    input_text = f"output/output_h_l_{args.loci}{add}.arp {args.permutation} {args.test}"
elif args.test == "AMOVA":
    input_text = f"output/output_amova_{args.loci}{add}.arp {args.permutation} {args.test}"

os.system(f"bash arlecore_linux/LaunchArlecore.sh {input_text}")