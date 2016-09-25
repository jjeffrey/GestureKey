import os
import sys
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def main():
    print "Type the name of the gesture you want to train or retrain to recognize."
    gestureName = sys.stdin.readline()[:-1]
    alldataP = np.zeros(1)
    alldataV = np.zeros(1)

    vData = []


    for file in os.listdir("testing/%s" % gestureName):
        if file.endswith("poss.npy"):
            newArr = np.load("testing/%s/%s" % (gestureName, file))
            print file
            print newArr
            vData.append(newArr)
            if np.size(alldataP) == 1:
                alldataP = newArr
            else:
                alldataP = np.concatenate((alldataP, newArr), axis=0)
        if file.endswith("vels.npy"):
            newArr = np.load("testing/%s/%s" % (gestureName, file))
            print file
            print newArr
            if np.size(alldataV) == 1:
                alldataV = newArr
            else:
                alldataV = np.concatenate((alldataV, newArr), axis=0)

    clusteringDataP = np.transpose(alldataP)

    clusteringDataV = np.transpose(alldataV)



    print "About how many segments does your gesture have?"
    cNum = sys.stdin.readline()[:-1]
    cNum = int(float(cNum))
    plt.figure(figsize=(12, 12))

    kms = KMeans(n_clusters=cNum).fit(alldataV)
    centroids = kms.cluster_centers_

    plt.subplot(221)
    plt.scatter(clusteringDataP[0,:], clusteringDataP[1, :], c=kms.predict(alldataV))

    #plt.subplot(221).plot(markeredgecolor="black")

    

    plt.subplot(222)
    plt.scatter(clusteringDataV[0,:], clusteringDataV[1, :], c=kms.predict(alldataV))
    #plt.subplot(222).plot(markeredgecolor="black")
    
    

    plt.scatter(centroids[:, 0], centroids[:, 1], s=300,
            marker='x', 
            linewidths=4,
            color='red', zorder=10)

    plt.show()

    print kms.predict(vData[1])

if __name__ == "__main__":
    main()
