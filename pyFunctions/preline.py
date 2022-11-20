import pandas as pd

def setUni(df):
    mySet = set()
    for idx, row in df.iterrows():
        mySet.add(row["uni"])
    return mySet

def distElement(dframe1, dframe2):
    set1 = setUni(dframe1)
    set2 = setUni(dframe2)
    diff = list(set2-set1)[0]
    myList = [
        dframe2.loc[dframe2['uni'] == diff, 'uni_id'].iloc[0],
        diff, "", "", ""]
    return myList


def appendDf(myDf, listDf, n):
    for val in range(n):
        toAppend = listDf[val]
        myDf = pd.concat([myDf, toAppend], ignore_index=True)
    return myDf

colnames = ["uni_id", "uni", "relative_scholarship", "paidfee", "perc_intern"]

df1 = (pd.read_csv("./data/output/2016.csv"))[colnames]
df2 = (pd.read_csv("./data/output/2017.csv"))[colnames]
df3 = (pd.read_csv("./data/output/2018.csv"))[colnames]
df4 = (pd.read_csv("./data/output/2019.csv"))[colnames]

newRowList = [
    pd.DataFrame(distElement(df3, df4), index = colnames).T,
    pd.DataFrame(distElement(df2, df3), index = colnames).T,
    pd.DataFrame(distElement(df1, df2), index = colnames).T
]

df1 = appendDf(df1, newRowList, 3)
df2 = appendDf(df2, newRowList, 2)
df3 = appendDf(df3, newRowList, 1)

outputCol = [
    "uni_id",
    "uni",
    "scholarship16",
    "scholarship17",
    "scholarship18",
    "scholarship19", 
    "paidfees16",
    "paidfees17",
    "paidfees18",
    "paidfees19",
    "intstuds16",
    "intstuds17",
    "intstuds18",
    "intstuds19"
]

finalDf = pd.DataFrame(columns=outputCol
)
for idx, row in df4.iterrows():
    iterId = row["uni_id"]
    row = [
        iterId,
        row["uni"],
        df1.loc[df1['uni_id'] == iterId, 'relative_scholarship'].iloc[0],
        df2.loc[df2['uni_id'] == iterId, 'relative_scholarship'].iloc[0],
        df3.loc[df3['uni_id'] == iterId, 'relative_scholarship'].iloc[0],
        row["relative_scholarship"],
        df1.loc[df1['uni_id'] == iterId, 'paidfee'].iloc[0],
        df2.loc[df2['uni_id'] == iterId, 'paidfee'].iloc[0],
        df3.loc[df3['uni_id'] == iterId, 'paidfee'].iloc[0],
        row["paidfee"],
        df1.loc[df1['uni_id'] == iterId, 'perc_intern'].iloc[0],
        df2.loc[df2['uni_id'] == iterId, 'perc_intern'].iloc[0],
        df3.loc[df3['uni_id'] == iterId, 'perc_intern'].iloc[0],
        row["perc_intern"]
    ]
    finalDf = pd.concat([finalDf, pd.DataFrame(row, index = outputCol).T], ignore_index=True)

#finalDf.to_csv("./data/output/forline.csv", index=False)

# Further code to create automatic HTML
for idx, row in finalDf.iterrows():
    htmltag = "<option value='{0}'>{0}</option>".format(row["uni"])
    print(htmltag)