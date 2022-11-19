import pandas as pd
import numpy as np
import statistics
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn import cluster

def listOfVal(series, parameter):
    outputList = [
        series["{0}_2016".format(parameter)],
        series["{0}_2017".format(parameter)],
        series["{0}_2018".format(parameter)],
        series["{0}_2019".format(parameter)],
    ]
    return outputList

def averageVal(df, parameter):
    outputList = []
    for idx, row in df.iterrows():
        val = statistics.fmean(listOfVal(row, parameter))
        outputList.append(val)
    df[parameter] = outputList
    return df

def getMemberCluster(df, html):
    outputList = []
    for idx, row in df.iterrows():
        if html:
            uni = str("<li>" + str(row["uni"]) + "</li>")
            outputList.append(uni)
        else:
            outputList.append(row["uni"])
    if html:
        outputStr = ""
        for el in outputList:
            outputStr = str(outputStr + el + "\n")
        return outputStr
    else:
        return outputList

# Create a single dataset with average values

df1 = pd.read_csv("data/output/2016.csv")
df2 = pd.read_csv("data/output/2017.csv")
df3 = pd.read_csv("data/output/2018.csv")
df4 = pd.read_csv("data/output/2017.csv")

df1 = df1.merge(df2, left_on='uni_id', right_on='uni_id', suffixes=('_2016', '_2017'))
df1 = df1.merge(df3, left_on='uni_id', right_on='uni_id', suffixes=('_2017', '_2018'))
df1 = df1.merge(df4, left_on='uni_id', right_on='uni_id', suffixes=('_2018', '_2019'))

df1 = averageVal(averageVal(averageVal(df1, "perc_intern"), "relative_scholarship"), "paidfee")

data = df1[["uni_2016", "relative_scholarship", "perc_intern", "paidfee"]].rename(columns={"uni_2016": "uni"})

X = data.iloc[:,1:4].values

# Apply elbow method to understand the number of cluster

wcss = []
for i in range(1,11):
    k_means = cluster.KMeans(n_clusters=i,init='k-means++', random_state=42)
    k_means.fit(X)
    wcss.append(k_means.inertia_) 

plt.plot(np.arange(1,11),wcss)
plt.xlabel('Clusters')
plt.ylabel('SSE')
# plt.show()

# Update the dataframe with the association university - cluster 

k_means_optimum = cluster.KMeans(n_clusters = 3, init = 'k-means++',  random_state=42)
y = k_means_optimum.fit_predict(X)

data['cluster'] = y 

# Parse and visualize clusters
data1 = data[data.cluster==0]
data2 = data[data.cluster==1]
data3 = data[data.cluster==2]

kplot = plt.axes(projection='3d')
xline = np.linspace(0, 15, 1000)
yline = np.linspace(0, 15, 1000)
zline = np.linspace(0, 15, 1000)
kplot.plot3D(xline, yline, zline, 'black')# Data for three-dimensional scattered points
kplot.scatter3D(data1.relative_scholarship, data1.perc_intern, data1.paidfee, c='red', label = 'Cluster 1')
kplot.scatter3D(data2.relative_scholarship, data2.perc_intern, data2.paidfee,c ='green', label = 'Cluster 2')
kplot.scatter3D(data3.relative_scholarship, data3.perc_intern, data3.paidfee, c='blue', label = 'Cluster 3')
plt.scatter(k_means_optimum.cluster_centers_[:,0], k_means_optimum.cluster_centers_[:,1], color = 'indigo', s = 200)
plt.legend()
plt.title("Kmeans")
# plt.show()

# Reference: https://medium.com/@sk.shravan00/k-means-for-3-variables-260d20849730

print(getMemberCluster(data3, True))