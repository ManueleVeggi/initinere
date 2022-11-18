import pandas as pd

df16 = pd.read_csv("data/output/2016.csv")
df17 = pd.read_csv("data/output/2017.csv")
df18 = pd.read_csv("data/output/2018.csv")
df19 = pd.read_csv("data/output/2019.csv")

print(df16.info())

def concatenateVal(colname):
    paidFee = pd.concat([
        df16[[colname]],
        df17[[colname]],
        df18[[colname]],
        df19[[colname]],
    ], ignore_index=True)
    return paidFee

#print(concatenateVal("paidfee"), concatenateVal("paidfee").mean())
#print(concatenateVal("scholarship"), concatenateVal("scholarship").mean())

def sumintern(colname):
    int16 = df16[colname].sum()
    int17 = df17[colname].sum()
    int18 = df18[colname].sum()
    int19 = df19[colname].sum()
    mySeries = pd.Series( (v for v in [int16, int17, int18, int19]) )
    return mySeries

print(sumintern("total_students"), sumintern("total_students").mean())