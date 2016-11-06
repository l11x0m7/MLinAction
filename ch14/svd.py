#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2015-10-25 17:19:33
# @Last Modified by:   anchen
# @Last Modified time: 2015-10-25 21:20:26


from numpy import *
from numpy import linalg as lg

def loadExData():
    return[[0, 0, 0, 2, 2],
           [0, 0, 0, 3, 3],
           [0, 0, 0, 1, 1],
           [1, 1, 1, 0, 0],
           [2, 2, 2, 0, 0],
           [5, 5, 5, 0, 0],
           [1, 1, 1, 0, 0]]

def loadExData2():
    return[[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
           [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
           [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
           [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
           [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
           [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
           [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
           [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
           [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
           [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
           [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]

def eulidSim(intA, intB):
    return 1.0/(1.0+lg.norm(intA-intB))

def pearsSim(intA, intB):
    if len(intA) < 3: return 1.0
    return 0.5 + 0.5*corrcoef(intA,intB,rowvar=0)[0][1]

def cosSim(intA, intB):
    num = float(intA.T*intB)
    length = lg.norm(intA)*lg.norm(intB)
    return 0.5+0.5*(num/length)

def standEst(dataMat, user, item, simMeas):
    n = shape(dataMat)[1]
    total = 0.0
    all_rate = 0.0
    for i in range(n):
        if dataMat[user,i]==0:continue
        overLap = nonzero(logical_and(dataMat[:,i].A>0, dataMat[:,item].A>0))[0]
        if len(overLap)==0:similarity=0.0
        else:
            similarity = simMeas(dataMat[overLap,i], dataMat[overLap, item])
        total += similarity
        all_rate += similarity*dataMat[user, i]
    if total==0:return 0.0
    return all_rate/total

def svdEst(dataMat, user, item, simMeas):
    n = shape(dataMat)[1]
    total = 0.0
    all_rate = 0.0
    U,Sigma,VT = lg.svd(dataMat)
    sig_mat = mat(eye(4)*Sigma[:4])
    svdItems = dataMat.T*U[:,:4]*sig_mat.I
    for i in range(n):
        if dataMat[user,i]==0:continue
        similarity = simMeas(svdItems[i,:].T, svdItems[item,:].T)
        total+=similarity
        all_rate+=similarity*dataMat[user,i]
    if total==0:return 0.0
    return all_rate/total

def recommend(dataMat, user, N=3, simMeas=cosSim, estMethod=standEst):
    wait_to_rate = nonzero(dataMat[user, :].A==0)[1]
    if len(wait_to_rate)==0:return "You've already rated all restaurants."
    score_list = []
    for item in wait_to_rate:
        score = estMethod(dataMat, user, item, simMeas)
        score_list.append((item, score))
    return sorted(score_list, key=lambda jj:jj[1], reverse=True)[:N]

def printMat(dataMat, thresh=0.8):
    for i in range(32):
        for j in range(32):
            if float(dataMat[i,j])>thresh:print 1,
            else:print 0,
        print ''

def imgCompress(numSV=3,thresh=0.8):
    fr = open(r'0_5.txt')
    image = []
    for line in fr:
        each_line = []
        for i in range(32):
            each_line.append(float(line[i]))
        image.append(each_line)
    print 'the original image is :'
    printMat(mat(image),thresh)
    U,Sigma,VT = lg.svd(image)
    mat_sig = mat(eye(numSV)*Sigma[:numSV])
    recover_image = U[:,:numSV]*mat_sig*VT[:numSV,:]    #32*3    3*3    3*32
    print 'the compressed image is :'
    printMat(mat(recover_image),thresh)

if __name__ == '__main__':
    # 1
    # data = mat(loadExData())
    # data[0,0]=data[0,1]=data[1,0]=data[2,0]=4
    # data[3,3]=2
    # print recommend(data, 2)
    #
    # 2
    # data = mat(loadExData2())
    # print recommend(data, 1,estMethod=svdEst)

    # 3
    imgCompress(4)
