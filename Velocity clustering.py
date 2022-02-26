import spacepy
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from matplotlib import pyplot, dates
from datetime import datetime
import tarfile
import urllib
from kneed import KneeLocator


import os
import numpy as np
import matplotlib.pyplot as plt
import _pickle as pickle
from spacepy import pycdf
from tslearn.metrics import dtw
from tslearn.clustering import TimeSeriesKMeans

def save_elements(list_e, name):
    f = file(name, 'w')
    for el in list_e:
        pickle.dump(el, f)
    f.close()


def read_elements(nb_el, name):
    f = file(name, 'r')
    list_el = []
    for el in range(nb_el):
        list_el.append(pickle.load(f))
    f.close()
    return list_el


def find_outlist(dir, dtype="cdf"):
    outlist = []
    for ff in os.listdir(dir):
        i = len(dtype) + 1
        if ff[-i:] == "." + dtype:
            outlist.append(ff)
    outlist.sort()
    return outlist


dir = "./"
list_files = find_outlist(dir, dtype="cdf")
x_axis = []
V = np.array([])
data_V = np.array([])
#data_Br = np.array([])
#data_Bt = np.array([])
#data_Bn = np.array([])


#Br=np.array([])
#Bt=np.array([])
#Bn=np.array([])
data_points=0

for ll in list_files:
    cdf = pycdf.CDF(dir + ll)
    td = cdf['Epoch'][:]
    rad_field = cdf['flowSpeed'][:]
    #rad_bfield=cdf['BR'][:]
    #tan_bfield=cdf['BT'][:]
    #nor_bfield=cdf['BN'][:]
    idx = []
    # This eliminates data gaps

    for ii in range(len(rad_field)):
        if (rad_field[ii] !=-9.999999848243207e+30 ):  # and (rad_bfield[ii] != -9.999999848243207e+30) and (nor_bfield[ii] != -9.999999848243207e+30) and (tan_bfield[ii] != -9.999999848243207e+30):
            idx.append(ii) # create array with integer x_axis instead of time variable
            x_axis.append(ii)
            data_points += 1
    # print(min(rad_bfield))
    # print(min(nor_bfield))
    # print(min(tan_bfield))
    V = np.append(V, np.array(rad_field[idx]))
    #Br=np.append(Br,np.array(rad_bfield[idx]))
    #Bt=np.append(Bt,np.array(tan_bfield[idx]))
    #Bn=np.append(Bn,np.array(nor_bfield[idx]))

# fig, (ax1) = plt.subplots(1)
# ax1.plot(x_axis,Bt)
# plt.show()

#plt.plot(x_axis,Bt)
#plt.plot(x_axis,Bn)
V1= V.reshape(-1,1) # reshape for 1-D arrays
#Br1= Br.reshape(-1,1)
#Bt1= Bt.reshape(-1,1)
#Bn1= Bn.reshape(-1,1)

for i in range(len(x_axis)-1):
    data_V = np.append(data_V, V[i])
    #data_Br = np.append(data_Br, Br[i])
    #data_Bt = np.append(data_Bt, Bt[i])
    #data_Bn = np.append(data_Bn, Bn[i])

kmeans_kwargs = {
    "init": "random",
    "n_init": 10,
    "max_iter": 300,
    "random_state": 42,
}

sse_V = []
for k in range(1, 20): # for 1-20 initial data clusters
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs) # unpack the dictionary into a cluster(k means function)
    kmeans.fit(V1) # standerize
    sse_V.append(kmeans.inertia_)
plt.style.use("fivethirtyeight") #plotting sse
plt.plot(range(1, 20), sse_V)
plt.xticks(range(1, 20))
plt.xlabel("Number of Clusters(V)")
plt.ylabel("SSE")
plt.show()
kl_V = KneeLocator( # algorithim for determining elbow point rather than looking at the graph (in the kneed package)
    range(1, 20), sse_V, curve="convex", direction="decreasing"
)

# sse_Br = []
# for k in range(1, 20): # for 1-20 initial data clusters
#     kmeans = KMeans(n_clusters=k, **kmeans_kwargs) # unpack the dictionary into a cluster(k means function)
#     kmeans.fit(Br1) # standerize
#     sse_Br.append(kmeans.inertia_)
# plt.style.use("fivethirtyeight") #plotting sse
# plt.plot(range(1, 20), sse_Br)
# plt.xticks(range(1, 20))
# plt.xlabel("Number of Clusters(V)")
# plt.ylabel("SSE")
# plt.show()
# kl_Br = KneeLocator( # algorithim for determining elbow point rather than looking at the graph (in the kneed package)
#     range(1, 20), sse_Br, curve="convex", direction="decreasing"
# )
#
# sse_Bt = []
# for k in range(1, 20): # for 1-20 initial data clusters
#     kmeans = KMeans(n_clusters=k, **kmeans_kwargs) # unpack the dictionary into a cluster(k means function)
#     kmeans.fit(Bt1) # standerize
#     sse_Bt.append(kmeans.inertia_)
# plt.style.use("fivethirtyeight") #plotting sse
# plt.plot(range(1, 20), sse_Bt)
# plt.xticks(range(1, 20))
# plt.xlabel("Number of Clusters(V)")
# plt.ylabel("SSE")
# plt.show()
# kl_Bt = KneeLocator( # algorithim for determining elbow point rather than looking at the graph (in the kneed package)
#     range(1, 20), sse_Bt, curve="convex", direction="decreasing"
# )
#
# sse_Bn = []
# for k in range(1, 20): # for 1-20 initial data clusters
#     kmeans = KMeans(n_clusters=k, **kmeans_kwargs) # unpack the dictionary into a cluster(k means function)
#     kmeans.fit(Bn1) # standerize
#     sse_Bn.append(kmeans.inertia_)
# plt.style.use("fivethirtyeight") #plotting sse
# plt.plot(range(1, 20), sse_Bn)
# plt.xticks(range(1, 20))
# plt.xlabel("Number of Clusters(V)")
# plt.ylabel("SSE")
# plt.show()
# kl_Bn = KneeLocator( # algorithim for determining elbow point rather than looking at the graph (in the kneed package)
#     range(1, 20), sse_Bn, curve="convex", direction="decreasing"
# )




print("Velocity Cluters: " + str(kl_V.elbow))
# print("Bt Cluters: " + str(kl_Br.elbow))
# print("Br Cluters: " + str(kl_Bt.elbow))
# print("Bn Cluters: " + str(kl_Bn.elbow))



kmeans = KMeans(init="random", n_clusters = kl_V.elbow, n_init = 10, random_state = 42)
kmeans.fit(V1) # fit to data in scaled features
plt.plot(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,0],'o')
fig, ax1 = plt.subplots(sharex=True, sharey=True)
fig.suptitle("Flow Speeds from ", fontsize=16)
fte_colors = {
    0: "#008fd5",
    1: "#fc4f30",
}
V_list = V1.tolist()
V1_list = []
final_data = []
for i in range(len(V_list)):
    V1_list += V_list[i]
    final_data.append([x_axis[i],V1_list[i]])
a_data = np.array(final_data)
print(a_data)
ax1.scatter(a_data[:,0], a_data[:,1], c=kmeans.labels_.astype(float))

#print(V)
plt.show()

# kmeans = KMeans(init="random", n_clusters = kl_Br.elbow, n_init = 10, random_state = 42)
# kmeans.fit(Br1) # fit to data in scaled features
# plt.plot(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,0],'o')
# fig, ax1 = plt.subplots(sharex=True, sharey=True)
# fig.suptitle("Flow Speeds from ", fontsize=16)
# Br_list = Br1.tolist()
# Br1_list = []
# final_data = []
# for i in range(len(Br_list)):
#     Br1_list += Br_list[i]
#     final_data.append([x_axis[i],Br1_list[i]])
# a_data = np.array(final_data)
# print(a_data)
# ax1.scatter(a_data[:,0], a_data[:,1], c=kmeans.labels_.astype(float))
#
# #print(V)
# plt.show()
#
# kmeans = KMeans(init="random", n_clusters = kl_Bt.elbow, n_init = 10, random_state = 42)
# kmeans.fit(V1) # fit to data in scaled features
# plt.plot(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,0],'o')
# fig, ax1 = plt.subplots(sharex=True, sharey=True)
# fig.suptitle("Flow Speeds from ", fontsize=16)
# Bt_list = Bt1.tolist()
# Bt1_list = []
# final_data = []
# for i in range(len(Bt_list)):
#     Bt1_list += Bt_list[i]
#     final_data.append([x_axis[i],Bt1_list[i]])
# a_data = np.array(final_data)
# print(a_data)
# ax1.scatter(a_data[:,0], a_data[:,1], c=kmeans.labels_.astype(float))
#
# #print(V)
# plt.show()
#
# kmeans = KMeans(init="random", n_clusters = kl_Bn.elbow, n_init = 10, random_state = 42)
# kmeans.fit(Bn1) # fit to data in scaled features
# plt.plot(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,0],'o')
# fig, ax1 = plt.subplots(sharex=True, sharey=True)
# fig.suptitle("Flow Speeds from ", fontsize=16)
# Bn_list = Bn1.tolist()
# Bn1_list = []
# final_data = []
# for i in range(len(Bn_list)):
#     Bn1_list += Bn_list[i]
#     final_data.append([x_axis[i],Bn1_list[i]])
# a_data = np.array(final_data)
# print(a_data)
# ax1.scatter(a_data[:,0], a_data[:,1], c=kmeans.labels_.astype(float))

#print(V)
plt.show()