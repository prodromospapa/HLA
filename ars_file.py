import argparse

parser = argparse.ArgumentParser(description='ARP file generator')
parser.add_argument('--test','-t', choices=["AMOVA","HL"] ,type=str, help='Type of test',required=True)
parser.add_argument('--permutation','-p', type=int, help='Number of permutations for AMOVA',required="-t"=="AMOVA")

args = parser.parse_args()

test = args.test
AMOVA_perm = args.permutation

with open("arlecore_linux/arl_run.ars") as r:
    with open('arlecore_linux/output.ars','w') as w:
        for line in r:
            if test == "HL":
                if line.startswith("MakeExactTestLD"):
                    w.write(f"MakeExactTestLD=1\n")
                elif line.startswith("ComputeDvalues"):
                    w.write(f"ComputeDvalues=1\n")
                elif line.startswith("MakeHWExactTest"):        
                    w.write(f"MakeHWExactTest=1\n")
                elif line.startswith("TaskNumber"):
                    w.write(f"TaskNumber=48\n")
                else:
                    w.write(line)
            elif test == "AMOVA":            
                if line.startswith("LocByLocAMOVA"):
                    w.write(f"LocByLocAMOVA=1\n")
                elif line.startswith("NumPermutationsAMOVA"):
                    w.write(f"NumPermutationsAMOVA={AMOVA_perm}\n")
                elif line.startswith("IncludeIndividualLevel"):
                    w.write(f"IncludeIndividualLevel=1\n")
                elif line.startswith("TaskNumber"):
                    w.write(f"TaskNumber=512\n")
                else:
                    w.write(line)