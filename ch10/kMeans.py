from numpy import *
def loadDataSet(filename):
    fr = open(filename)
    dataMat = []
    for line in fr:
        curline = line.strip().split('\t')
        fltline = map(float, curline)
        dataMat.append(fltline)
    return mat(dataMat)

def defaultMeas(inA, inB):
    return sqrt(sum(power((inA-inB),2)))

def randCen(dataMat, k):
    n = shape(dataMat)[1]
    center = mat(zeros((k,n)))
    for i in range(n):
        minJ = min(dataMat[:,i])
        rangeJ = float(max(dataMat[:,i])-minJ)
        center[:,i] = minJ + rangeJ*random.rand(k,1)
    return center

def kMeans(dataMat, k, distMeas=defaultMeas, clusterCen=randCen):
    m = shape(dataMat)[0]
    cur_center = clusterCen(dataMat, k)
    clusterAssment = mat(zeros((m,2)))
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            mindis = inf
            mincenter=-1
            for j in range(k):
                distance = distMeas(dataMat[i,:], cur_center[j,:])
                if distance<mindis:
                    mindis=distance
                    mincenter=j
            if mincenter!=clusterAssment[i,0]:
                clusterChanged=True
            clusterAssment[i,:] = mincenter, mindis**2
        print cur_center
        for i in range(k):
            if len(nonzero(clusterAssment[:,0]))!=0:
                cur_center[i,:] = mean(dataMat[nonzero(clusterAssment[:,0].A==i)[0]],axis=0)
    return cur_center, clusterAssment

def draw(data1,data2):
    from matplotlib import pyplot as plt
    pic = plt.figure()
    ax = pic.add_subplot(111)
    ax.scatter(data1[:,0].flatten().A[0],data1[:,1].flatten().A[0],c='r', s=50)
    ax.scatter(data2[:,0].flatten().A[0],data2[:,1].flatten().A[0],c='g', s=50,marker='^')
    pic.show()

def biKmeans(dataMat, k, distMeas=defaultMeas):
    m = shape(dataMat)[0]
    cur_center=mean(dataMat,axis=0).tolist()[0]
    clusterAssment = mat(zeros((m,2)))
    centerList = []
    centerList.append(cur_center)
    for i in range(m):
        clusterAssment[i,1]=distMeas(mat(cur_center),dataMat[i,:])**2
    while len(centerList)<k:
        lowestSSE=inf
        for i in range(len(centerList)):
            cur_data = dataMat[nonzero(clusterAssment[:,0].A==i)[0],:]
            if len(cur_data)==0:
                continue
            cur_center, cur_cluster = kMeans(cur_data,2)
            split_SSE = sum(cur_cluster[:,1])
            dissplit_SSE = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])
            print split_SSE, dissplit_SSE
            if (split_SSE+dissplit_SSE)<lowestSSE:
                lowestSSE=split_SSE+dissplit_SSE
                best_cluster = cur_cluster
                best_center=cur_center
                best_to_split = i
        print 'the best center to split is :%d' % (best_to_split,)
        best_cluster[nonzero(best_cluster[:,0].A==1)[0],0]=len(centerList)
        best_cluster[nonzero(best_cluster[:,0].A==0)[0],0]=best_to_split
        centerList[best_to_split] = best_center[0,:].tolist()[0]
        centerList.append(best_center[1,:].tolist()[0])
        clusterAssment[nonzero(clusterAssment[:,0].A==best_to_split)[0],:]=best_cluster
    return mat(centerList), clusterAssment

def distSLC(vecA, vecB):#Spherical Law of Cosines
    a = sin(vecA[0,1]*pi/180) * sin(vecB[0,1]*pi/180)
    b = cos(vecA[0,1]*pi/180) * cos(vecB[0,1]*pi/180) * \
                      cos(pi * (vecB[0,0]-vecA[0,0]) /180)
    return arccos(a + b)*6371.0 #pi is imported with numpy

import matplotlib
import matplotlib.pyplot as plt
def clusterClubs(numClust=5):
    datList = []
    for line in open(r'places.txt').readlines():
        lineArr = line.split('\t')
        datList.append([float(lineArr[4]), float(lineArr[3])])
    datMat = mat(datList)
    myCentroids, clustAssing = biKmeans(datMat, numClust, distMeas=distSLC)
    fig = plt.figure()
    rect=[0.1,0.1,0.8,0.8]
    scatterMarkers=['s', 'o', '^', '8', 'p', \
                    'd', 'v', 'h', '>', '<']
    axprops = dict(xticks=[], yticks=[])
    ax0=fig.add_axes(rect, label='ax0', **axprops)
    imgP = plt.imread('Portland.png')
    ax0.imshow(imgP)
    ax1=fig.add_axes(rect, label='ax1', frameon=False)
    for i in range(numClust):
        ptsInCurrCluster = datMat[nonzero(clustAssing[:,0].A==i)[0],:]
        markerStyle = scatterMarkers[i % len(scatterMarkers)]
        ax1.scatter(ptsInCurrCluster[:,0].flatten().A[0], ptsInCurrCluster[:,1].flatten().A[0], marker=markerStyle, s=90)
    ax1.scatter(myCentroids[:,0].flatten().A[0], myCentroids[:,1].flatten().A[0], marker='+', s=300)
    plt.show()

if __name__ == '__main__':
    # 1
    # dataMat = loadDataSet(r'testSet.txt')
    # myCentroids, clustAssing = kMeans(dataMat, 3)
    # draw(dataMat, myCentroids)

    # 2
    # dataMat = loadDataSet(r'testSet2.txt')
    # centerList, myNewAssments = biKmeans(dataMat,3)
    # draw(dataMat, centerList)

    # 3
    # clusterClubs()
