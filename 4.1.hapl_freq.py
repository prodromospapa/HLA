import os
import argparse


parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--loci','-l', type=str,choices=['3','5'], help='Number of loci',required='-d'=="Greece")
parser.add_argument('--database','-d', type=str,choices=["Greece","DKMS"], help='database to use', required=True)
parser.add_argument('--total','-to', action='store_true', help='Total of database', required=False)

args = parser.parse_args()

if not os.path.exists('bootstrap'):
    os.makedirs('bootstrap')
    
if args.total:
    total = "_total"
else:
    total = ""

if args.database == "Greece":
    os.system(f"cp output/output_{args.loci}{total}.arp bootstrap/")
    input_text = f"bootstrap/output_{args.loci}{total}.arp"

else:
    os.system(f"cp output/output_dkms{total}.arp bootstrap/")
    input_text = f"bootstrap/output_dkms{total}.arp"


os.system(f"bash arlecore_linux/LaunchArlecore.sh {input_text} FREQ")


