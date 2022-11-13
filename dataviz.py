import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn import cluster

def floatConvert(pdDf): #easy conversion into float
    for idx, row in pdDf.iterrows(): 
        val1 = str(row["paidfee"]); val2 = str(row["totalfee"])
        pdDf.at[idx, "paidfee"] = val1.replace(',', '.')
        pdDf.at[idx, "totalfee"] = val2.replace(',', '.')
    pdDf['paidfee'] = pdDf['paidfee'].astype(float)
    pdDf['totalfee'] = pdDf['totalfee'].astype(float)
    return pdDf

df = floatConvert(pd.read_csv("data/output/2016.csv"))

Xuni = df[['uni']]
Yfee = df[['paidfee']]
Zdsu = df[['relative_scholarship']]

X_axis = np.arange(len(Xuni))
  
plt.bar(X_axis - 0.2, Yfee, 0.4, label = 'Paid fee')
plt.bar(X_axis + 0.2, Zdsu, 0.4, label = 'Average scholarship for students')
  
plt.xticks(X_axis, Xuni)
plt.xlabel("University")
plt.ylabel("Euro")
plt.title("Fee vs DSU")
plt.legend()
plt.show()

"""
wcss = []
X = df[['relative_scholarship', 'paidfee']].copy()

for i in range(1, 11): 
    kmeans = cluster.KMeans(n_clusters=i, random_state=0)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

sns.set()

# plt.plot(range(1, 11), wcss)
# plt.title('Selecting the Numbeer of Clusters using the Elbow Method')
# plt.xlabel('Clusters')
# plt.ylabel('WCSS')
# plt.show() # Elbow methods reveals that best number of centroids is 3

kmeans = cluster.KMeans(n_clusters=3, init='k-means++', max_iter=500, n_init=20, random_state=0)
y_pred = kmeans.fit_predict(X)
plt.scatter(X['relative_scholarship'], X['paidfee'])
plt.ylabel("paidfee")
plt.xlabel("relative_scholarship")
plt.title("Clusters found by KMeans")
plt.show()
"""