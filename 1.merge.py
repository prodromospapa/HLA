import pandas as pd
import pickle

def merge1(BMD_3, BMD_5,CBU_3,CBU_5,no_D,no_D_elidek,elidek):
    data_BMD_3 = pd.read_excel(BMD_3) #here we have to change column names according to the others
    data_BMD_5 = pd.read_excel(BMD_5)
    data_CBU_3 = pd.read_excel(CBU_3)
    data_CBU_5 = pd.read_excel(CBU_5)

    only_BMD_3 = data_BMD_3.loc[~data_BMD_3.index.isin(data_BMD_5.index)]
    only_CBU_3 = data_CBU_3.loc[~data_CBU_3.index.isin(data_CBU_5.index)]
    source = ["BMD"]*data_BMD_5.shape[0] + ["CBU"]*data_CBU_5.shape[0] + ["BMD"]*only_BMD_3.shape[0] + ["CBU"]*only_CBU_3.shape[0]
    loci = [5]*(data_BMD_5.shape[0]+data_CBU_5.shape[0]) + [3]*(only_BMD_3.shape[0]+only_CBU_3.shape[0])
    merged_data = pd.concat([data_BMD_5,data_CBU_5,only_BMD_3,only_CBU_3,])
    merged_data["source"] = source
    merged_data["loci"] = loci
    if elidek:
        correct_id = pd.read_excel(no_D_elidek)["ID"]
    else:
        correct_id = pd.read_excel(no_D)['ID']
    merged_data = merged_data[merged_data["ID"].isin(correct_id)]
    return merged_data
    
def merge2(data):
    loci_dict = {"A":["A1","A2"],"B":["B1","B2"],"C":["C1","C2"],"DRB1":["DRB1_1","DRB1_2"],"DQB1":["DQB1_1","DQB1_2"]}

    alleles_dict = {}
    for locus in loci_dict:
        alleles_locus = set(sorted(data[loci_dict[locus][0]].dropna().values.tolist() + data[loci_dict[locus][1]].dropna().values.tolist()))
        alleles_dict[locus] = {}
        n = 1
        for allele in alleles_locus:
            alleles_dict[locus][allele] = n
            n += 1

    final = pd.DataFrame(data[["ID","source","loci"]])
    original = pd.DataFrame(data[["ID","source","loci"]])
    for locus,alleles in loci_dict.items():
        final[locus] = data[loci_dict[locus]].apply(lambda x: set(sorted([alleles_dict[locus][i] for i in x if i in alleles_dict[locus]])), axis=1)
        original[locus] = data[loci_dict[locus]].apply(lambda x: set(sorted([i for i in x if i in alleles_dict[locus]])), axis=1)
        #final[alleles[0]] = data[alleles[0]].apply(lambda x: alleles_dict[locus][x] if x in alleles_dict[locus] else 0)
        #final[alleles[1]] = data[alleles[1]].apply(lambda x: alleles_dict[locus][x] if x in alleles_dict[locus] else 0)
    

    final.reset_index(drop=True).to_pickle("all.pickle")
    original.reset_index(drop=True).to_pickle("all_original.pickle")

BMD_3 = "data/3_loci/75599_2_fields_77785BMDs_3loci_excl.blanks050424.xlsx"
BMD_5 = "data/5_loci/69130_Greek77785BMDs_2fields_5loci_final050424.xlsx"
CBU_3 = "data/3_loci/3012_2field_3019CBUs_3loci_excl.bl_haplomat.xlsx"
CBU_5 = "data/5_loci/1092_2fields_CBUs_5loci_excl.bl.xlsx"
no_D = "data/Extra_Analyses_Greek_CBUs_BMDs_80804_noD_no124.xlsx"
no_D_elidek = "data/ΕΛΙΔΕΚ_GREEK_CBUs_BMDs_80706_noD_no124.xlsx"



data = merge1(BMD_3, BMD_5,CBU_3,CBU_5,no_D,no_D_elidek,elidek=False)
merge2(data)

