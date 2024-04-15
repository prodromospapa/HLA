import pandas as pd
import argparse

def merge(BMD_3, BMD_5,CBU_3,CBU_5,choose):
    data_BMD_3 = pd.read_excel(BMD_3, index_col=0) #here we have to change column names according to the others
    data_BMD_5 = pd.read_excel(BMD_5, index_col=0)
    data_CBU_3 = pd.read_excel(CBU_3, index_col=0).drop(columns=["BIRTH"])
    data_CBU_5 = pd.read_excel(CBU_5, index_col=0).drop(columns=["BIRTH"])

    only_BMD_3 = data_BMD_3.loc[~data_BMD_3.index.isin(data_BMD_5.index)]
    only_CBU_3 = data_CBU_3.loc[~data_CBU_3.index.isin(data_CBU_5.index)]

    if choose == "BMD":
        merged_data = pd.concat([data_BMD_5,only_BMD_3])
        merged_data.to_pickle("BMD.pickle")
    elif choose == "CBU":
        merged_data = pd.concat([data_CBU_5,only_CBU_3])
        merged_data.to_pickle("CBU.pickle")
    else:
        merged_data = pd.concat([data_BMD_5,data_CBU_5,only_CBU_3,only_BMD_3])
        merged_data.to_pickle("all.pickle")


BMD_3 = "data/Greek_BMDs_2fields/76689gen_2_fields_BMDs_3loci_excl.blanks.xlsx"
BMD_5 = "data/Greek_BMDs_2fields/70077gen_78716BMDs_2fields_5loci_excl.bl.xlsx"
CBU_3 = "data/Greek_CBUs_2fields/3012gen_2field_CBUs_3loci_excl.bl.xlsx"
CBU_5 = "data/Greek_CBUs_2fields/1092gen_2fields_CBUs_5loci_excl.bl.xlsx"

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--choose','-c', choices=['BMD','CBU','all'], help='Direction(GvH or HvG)', required=True)

args = parser.parse_args()

merge(BMD_3, BMD_5,CBU_3,CBU_5, args.choose)