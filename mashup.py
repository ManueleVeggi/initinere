from sqlite3 import connect
from pandas import read_csv, read_sql, DataFrame
import pandas as pd
import re

raw_dsu16 = pd.read_csv("data/dsu2016.csv", sep=";", encoding = "ISO-8859-1")
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

#dsu16.drop_duplicates(ignore_index=True, inplace=True)
#print(dsu16)
    



