import pandas as pd

def mergeCount(sourceDf, destDf, idcol, namecol, valcol):
    i = 0
    for idx, row in sourceDf.iterrows():
        destDf.at[i, [1]] = row[idcol]  
        destDf.at[i, [2]] = row[namecol]
        temp = sourceDf.query('{0} == "{1}"'.format(idcol, row[idcol]))
        sum = 0
        for tempidx, temprow in temp.iterrows():
            sum += int(temprow[valcol])
        destDf.at[i, [3]] = sum
        i += 1
    destDf.drop_duplicates(ignore_index=True, inplace=True)
    return destDf

def refineStudId(myDf):
    for idx, row in myDf.iterrows():
        while len(str(row["AteneoCOD"])) < 4:
            row["AteneoCOD"] = str(row["AteneoCOD"]) + "0"
        myDf.at[idx, "AteneoCOD"] = str(row["AteneoCOD"])
        return myDf

def dataligner(dsupath, feepath, studpath, intpath, year, outputpath):
    
    #FASE 1
    #Creates source dataframes from csv
    dsuRaw = pd.read_csv(dsupath, sep=";", encoding = "ISO-8859-1")
    feeRaw = pd.read_csv(feepath, sep=",", encoding = "ISO-8859-1")
    studentRaw = pd.read_csv(studpath, sep=",", encoding = "ISO-8859-1").query('AnnoA == "{0}"'.format(year))
    intstudRaw = pd.read_csv(intpath, sep=",", encoding = "ISO-8859-1").query('AnnoA == "{0}"'.format(year))
    
    #Defines two intermediate and one last output dataframes
    dsuDf = pd.DataFrame(columns=["uni_id", "university", "scholarship"])
    studDf = pd.DataFrame(columns=["uni_id", "uni", "total_students"])
    outputDf = pd.DataFrame(columns=["uni_id", "uni", "total_students", "int_students", "perc_intern"])

    #FASE 2
    #Clean dataframe about "Diritto allo studio", aka scholarships
    dsuRaw = dsuRaw.query('TIPO_ISTITUTO == "Ateneo"')

    #Do not consider telematic university, simplify redundant records, uniform the ids
    for idx, row in dsuRaw.iterrows():
        if "telematic" not in row[6]:
            if "<" in row[6]:
                row[6] = (row[6].split("<"))[0]
            elif "(" in row[6]:
                row[6] = (row[6].split("("))[0]
            row[5]= str(row[5])
            while len(str(row[5])) < 6:
                row[5] = str(str(row[5]) + "0")
            dsuRaw.at[idx, "CODICE_ISTITUTO"] = row[5][:-2:]

    dsuDf = mergeCount(dsuRaw, dsuDf, "CODICE_ISTITUTO", "NOME_ISTITUTO", "SPESA_LAUREA")

    #FASE 3
    #Refine and uniform the ids in the fees dataframe
    for idx, row in feeRaw.iterrows():
        while row["COD_Ateneo"].startswith("0"):
            row["COD_Ateneo"] = row["COD_Ateneo"][1:]
        while len(str(row["COD_Ateneo"])) < 4:
            row["COD_Ateneo"] = str(row["COD_Ateneo"]) + "0"
        feeRaw.at[idx, "COD_Ateneo"] = row["COD_Ateneo"]

    #Merge scholarships and fees
    dsuDf = pd.merge(dsuDf, feeRaw, how='inner',left_on='uni_id',right_on='COD_Ateneo')
    dsuDf = dsuDf[['uni_id', 'NOME_ATENEO', 'scholarship', 'TASSA_MEDIA_PAGANTI_LAUREA', 'TASSA_MEDIA_TOTALE_ISCRITTI_LAUREA']].rename(columns= {'NOME_ATENEO':'uni', 'TASSA_MEDIA_PAGANTI_LAUREA':'paidfee','TASSA_MEDIA_TOTALE_ISCRITTI_LAUREA':'totalfee'})
    dsuDf.drop_duplicates(ignore_index=True, inplace=True)

    #FASE 4
    #Apply similar processes for overall enrolling
    studentRaw = refineStudId(studentRaw)
    studDf = mergeCount(studentRaw, studDf, "AteneoCOD", "AteneoNOME", "Isc")
    studDf = pd.merge(dsuDf, studDf, how='inner',left_on='uni_id',right_on='uni_id')
    studDf = studDf[['uni_id', 'uni_y', 'scholarship', 'paidfee', 'totalfee', 'total_students']].rename(columns= {'uni_y':'uni'})

    #Apply similar processes for international enrolling
    intstudRaw = refineStudId(intstudRaw)
    outputDf = mergeCount(intstudRaw, studDf, "AteneoCOD", "AteneoNOME", "Isc_S") 
    outputDf = pd.merge(outputDf, studDf, how='inner',left_on='uni_id',right_on='uni_id')
    outputDf = outputDf[['uni_id', 'uni_y', 'scholarship', 'paidfee', 'totalfee', 'total_students_y', 'int_students', 'perc_intern']].rename(columns= {'uni_y':'uni','total_students_y':'total_students'})

    #Compute percentages of international students
    for idx, row in outputDf.iterrows():
        outputDf.at[idx, "perc_intern"] = 100 * int(row["int_students"])/int(row["total_students"])
    
    #FASE 6
    #Export the dataframe
    outputDf.to_csv(outputpath, index=False)
    return outputDf

dsu2016 = "data/dsu2016.csv"
fee2016 = "data/fees2016.csv"
stud2016 = "data/student.csv"
ints2016 = "data/intStudent.csv"
dest2016 = "data/output/2016.csv"

print(dataligner(dsu2016, fee2016, stud2016, ints2016, "2015/2016", dest2016))






