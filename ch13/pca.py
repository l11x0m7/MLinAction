#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2015-10-25 15:38:20
# @Last Modified by:   anchen
# @Last Modified time: 2015-10-25 17:12:17

from numpy import *

def loadDataSet(filepath, delim='\t'):
    fr = open(filepath,'r')
    stringMat = [line.strip().split(delim) for line in fr]
    dataMat = [map(float, line) for line in stringMat]
    fr.close()
    return mat(dataMat)

def pca(dataMat, topNfeet=999999):
    data_mean = mean(dataMat,axis=0)
    mean_removed = dataMat - data_mean
    covMat = cov(mean_removed, rowvar=0)
    eigVals, eigVector = linalg.eig(mat(covMat))
    eig_ind = argsort(eigVals)
    eig_ind = eig_ind[:-(topNfeet+1):-1]
    eig_vec = eigVector[:,eig_ind]
    low_data = mean_removed*eig_vec
    rec_data = low_data*eig_vec.T + data_mean
    return rec_data, low_data

def paint(dataMat1,dataMat2, mark='o', size=50, color='r'):
    from matplotlib import pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(dataMat1[:,0].flatten().A[0], dataMat1[:,1].flatten().A[0], marker=mark,s=size,c=color)
    ax.scatter(dataMat2[:,0].flatten().A[0], dataMat2[:,1].flatten().A[0], marker='^',s=50,c='b')
    fig.show()

def transNanToMean():
    dataMat = loadDataSet(r'secom.data', ' ')
    n = shape(dataMat)[1]
    for feat in range(n):
        data_mean = mean(dataMat[nonzero(~isnan(dataMat[:,feat].A))[0],feat],axis=0)
        dataMat[nonzero(isnan(dataMat[:,feat].A))[0],feat] = data_mean
    return dataMat

if __name__ == '__main__':
    # 1
    # data = loadDataSet(r'testSet.txt')
    # Rec, Low = pca(data, 1)
    # paint(data,Rec, 'o', 50, 'g')

    # 2
    data = transNanToMean()
    rec_data, low_data = pca(data)
