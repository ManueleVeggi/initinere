import pandas as pd

raw_dsu16 = pd.read_csv("data/dsu2016.csv", sep=";", encoding = "ISO-8859-1")
raw_fee16 = pd.read_csv("data/fees2016.csv", sep=",", encoding = "ISO-8859-1")
student16 = pd.read_csv("data/student.csv", sep=",", encoding = "ISO-8859-1").query('AnnoA == "2015/2016"')
intstud16 = pd.read_csv("data/intStudent.csv", sep=",", encoding = "ISO-8859-1").query('AnnoA == "2015/2016"')

dsu16 = pd.DataFrame(columns=["uni_id", "university", "scholarship"])
students = pd.DataFrame(columns=["uni_id", "uni", "total_students"])
outputDf = pd.DataFrame(columns=["uni_id", "uni", "total_students", "int_students", "perc_intern"])

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
        row["COD_Ateneo"] = str(row["COD_Ateneo"]) + "0"
    raw_fee16.at[idx, "COD_Ateneo"] = row["COD_Ateneo"]

dsu16 = pd.merge(dsu16, raw_fee16, how='inner',left_on='uni_id',right_on='COD_Ateneo')
dsu16 = dsu16[['uni_id', 'NOME_ATENEO', 'scholarship', 'TASSA_MEDIA_PAGANTI_LAUREA', 'TASSA_MEDIA_TOTALE_ISCRITTI_LAUREA']].rename(columns= {'NOME_ATENEO':'uni', 'TASSA_MEDIA_PAGANTI_LAUREA':'paidfee','TASSA_MEDIA_TOTALE_ISCRITTI_LAUREA':'totalfee'})
dsu16.drop_duplicates(ignore_index=True, inplace=True)

# STUDENTS

for idx, row in student16.iterrows():
    while len(str(row["AteneoCOD"])) < 4:
        row["AteneoCOD"] = str(row["AteneoCOD"]) + "0"
    student16.at[idx, "AteneoCOD"] = str(row["AteneoCOD"])

i = 0
for idx, row in student16.iterrows():
    students.at[i, "uni_id"] = row["AteneoCOD"]
    students.at[i, "uni"] = row["AteneoNOME"]
    temp = student16.query("AteneoCOD == '{0}'".format(row["AteneoCOD"]))
    sum = 0
    for tempidx, temprow in temp.iterrows():
        sum += int(temprow["Isc"])
    students.at[i, "total_students"] = sum
    i += 1

students.drop_duplicates(ignore_index=True, inplace=True)
students = pd.merge(dsu16, students, how='inner',left_on='uni_id',right_on='uni_id')
students = students[['uni_id', 'uni_y', 'scholarship', 'paidfee', 'totalfee', 'total_students']].rename(columns= {'uni_y':'uni'})

# INTSTUDENT

for idx, row in intstud16.iterrows():
    while len(str(row["AteneoCOD"])) < 4:
        row["AteneoCOD"] = str(row["AteneoCOD"]) + "0"
    intstud16.at[idx, "AteneoCOD"] = str(row["AteneoCOD"])

for idx, row in intstud16.iterrows():
    outputDf.at[i, "uni_id"] = row["AteneoCOD"]
    outputDf.at[i, "uni"] = row["AteneoNOME"]
    temp = intstud16.query("AteneoCOD == '{0}'".format(row["AteneoCOD"]))
    sum = 0
    for tempidx, temprow in temp.iterrows():
        sum += int(temprow["Isc_S"])
    outputDf.at[i, "int_students"] = sum
    i += 1

outputDf.drop_duplicates(ignore_index=True, inplace=True)
outputDf = pd.merge(outputDf, students, how='inner',left_on='uni_id',right_on='uni_id')
outputDf = outputDf[['uni_id', 'uni_y', 'scholarship', 'paidfee', 'totalfee', 'total_students_y', 'int_students', 'perc_intern']].rename(columns= {'uni_y':'uni','total_students_y':'total_students'})

for idx, row in outputDf.iterrows():
    outputDf.at[idx, "perc_intern"] = 100 * int(row["int_students"])/int(row["total_students"])
print(outputDf)
outputDf.to_csv("data/output/2016.csv", index=False)