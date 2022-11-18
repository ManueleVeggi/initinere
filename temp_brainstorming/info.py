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


#Following code shows that df are not same legth even at the beginning

""" #code
def compare(d1, d2, d3, d4, year):
    df1 = pd.read_csv(d1, sep=";", encoding = "ISO-8859-1")
    df2 = pd.read_csv(d2, sep=";", encoding = "ISO-8859-1")
    df3 = pd.read_csv(d3, sep=",", encoding = "ISO-8859-1").query('AnnoA == "{0}"'.format(year))
    df4 = pd.read_csv(d4, sep=",", encoding = "ISO-8859-1").query('AnnoA == "{0}"'.format(year))
    print(year)
    d = {
        "dsu": len(df1),
        "fee": len(df2),
        "stu": len(df3),
        "int": len(df4)
    }
    return d

stud = "data/student.csv"
ints = "data/intStudent.csv"

dsu2016 = "data/dsu2016.csv"
fee2016 = "data/fees2016.csv"
dest2016 = "data/output/2016.csv"

dsu2017 = "data/dsu2017.csv"
fee2017 = "data/fees2017.csv"
dest2017 = "data/output/2017.csv"

dsu2018 = "data/dsu2018.csv"
fee2018 = "data/fees2018.csv"
dest2018 = "data/output/2018.csv"

dsu2019 = "data/dsu2019.csv"
fee2019 = "data/fees2019.csv"
dest2019 = "data/output/2019.csv"

print(compare(dsu2016, fee2016, stud, ints, "2015/2016"))
print("*****************")
print(compare(dsu2017, fee2017, stud, ints, "2016/2017"))
print("*****************")
print(compare(dsu2018, fee2018, stud, ints, "2017/2018"))
print("*****************")
print(compare(dsu2019, fee2019, stud, ints, "2018/2019"))
"""

""" #results
2015/2016
{'dsu': 3470, 'fee': 99, 'stu': 182, 'int': 91}
*****************
2016/2017
{'dsu': 3582, 'fee': 100, 'stu': 182, 'int': 91}
*****************
2017/2018
{'dsu': 4074, 'fee': 100, 'stu': 182, 'int': 91}
*****************
2018/2019
{'dsu': 4072, 'fee': 95, 'stu': 184, 'int': 92}
"""