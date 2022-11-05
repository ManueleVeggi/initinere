import pandas as pd

raw_dsu16 = pd.read_csv("data/dsu2016.csv", sep=";", encoding = "ISO-8859-1")
raw_fee16 = pd.read_csv("data/fees2016.csv", sep=",", encoding = "ISO-8859-1")
dsu16 = pd.DataFrame(columns=["uni_id", "university", "scholarship"])

#Clean the dataframe: remove comments, simplify codes

raw_dsu16 = raw_dsu16.query('TIPO_ISTITUTO == "Ateneo"')
for idx, row in raw_dsu16.iterrows():
    if "telematic" not in row[6]:
        if "<" in row[6]:
            row[6] = (row[6].split("<"))[0]
        elif "(" in row[6]:
            row[6] = (row[6].split("("))[0]
        row[5]= str(row[5])
        while len(str(row[5])) < 6:
            row[5] = str(str(row[5]) + "0")
        raw_dsu16.at[idx, "CODICE_ISTITUTO"] = row[5][:-2:]


i = 0
for idx, row in raw_dsu16.iterrows():
    dsu16.at[i, "uni_id"] = row[5]
    dsu16.at[i, "university"] = row[6]
    temp = raw_dsu16.query('CODICE_ISTITUTO == "{0}"'.format(row[5]))
    sum = 0
    for tempidx, temprow in temp.iterrows():
        sum += int(temprow["SPESA_LAUREA"])
    dsu16.at[i, "scholarship"] = sum
    i += 1

dsu16.drop_duplicates(ignore_index=True, inplace=True)
for idx, row in raw_fee16.iterrows():
    while row["COD_Ateneo"].startswith("0"):
        row["COD_Ateneo"] = row["COD_Ateneo"][1:]
    while len(str(row["COD_Ateneo"])) < 4:
        row["COD_Ateneo"] = str(str(row["COD_Ateneo"]) + "0")
    raw_fee16.at[idx, "COD_Ateneo"] = row["COD_Ateneo"]

dsu16 = pd.merge(dsu16, raw_fee16, how='inner',left_on='uni_id',right_on='COD_Ateneo')
dsu16 = dsu16[['uni_id', 'NOME_ATENEO', 'scholarship', 'TASSA_MEDIA_PAGANTI_LAUREA', 'TASSA_MEDIA_TOTALE_ISCRITTI_LAUREA']].rename(columns= {'NOME_ATENEO':'uni', 'TASSA_MEDIA_PAGANTI_LAUREA':'paidfee','TASSA_MEDIA_TOTALE_ISCRITTI_LAUREA':'totalfee'})
print(dsu16)