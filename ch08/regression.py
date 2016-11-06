#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2015-09-30 21:15:13
# @Last Modified by:   anchen
# @Last Modified time: 2015-10-02 17:09:09

from numpy import *
from time import sleep
import json
import urllib2

def loadDataSet(filename):
    dataMat = []
    labelMat = []
    fr = open(filename)
    numFeat = len(open(filename).readline().split('\t')) - 1
    for line in fr.readlines():
        data = []
        cur_line = line.strip().split('\t')
        for i in range(numFeat):
            data.append(float(cur_line[i]))
        dataMat.append(data)
        labelMat.append([float(cur_line[-1])])
    return dataMat, labelMat

def standRegress(xArr, yArr):
    xMat = mat(xArr)
    yMat = mat(yArr)
    xTx = xMat.T * xMat
    if linalg.det(xTx) == 0:
        print 'This matrix is singular, cannot do inverse'
        return
    ws = xTx.I * xMat.T * yMat      #(n,n) * (n,m) * (m,1) = (n,1)
    return ws

def plotLR(xArr, yArr, ws):
    import matplotlib.pyplot as plt
    xMat = mat(xArr)
    yMat = mat(yArr)
    fg = plt.figure()
    fg.clf()
    ax = fg.add_subplot(111)
    ax.scatter(xMat[:, 1].flatten().A[0], yMat[:, 0].flatten().A[0])
    xCopy = xMat.copy()
    xCopy.sort(0)                #sort(0)用来将xCopy中的数按照列分别进行排序（默认按行（-1），此时按列（0）），从小到大。
    yHat = xCopy * ws
    ax.plot(xCopy[:,1], yHat)
    plt.show()

def lwlr(testPoint, xArr, yArr, k = 1.0):
    xMat = mat(xArr)
    yMat = mat(yArr)
    m, n = shape(xMat)
    weights = mat(eye((m)))
    for i in range(m):
        x_diff = testPoint - xMat[i, :]
        weights[i,i] = exp(x_diff * x_diff.T/(-2.0*k**2))
    xTx = xMat.T * weights * xMat
    if linalg.det(xTx) == 0:
        print 'This matrix is singular, cannot do inverse'
        return
    ws = xTx.I * xMat.T * weights * yMat
    return testPoint * ws

def testLwlr(testArr, xArr, yArr, k=1.0):
    m = shape(testArr)[0]
    yHat = zeros((m,1))
    for i in range(m):
        yHat[i, 0] = lwlr(testArr[i], xArr, yArr, k)
    return yHat

def plotLWLR(xArr, yArr, yHat ):
    import matplotlib.pyplot as plt
    xMat = mat(xArr)
    yMat = mat(yArr)
    xInd = xMat[:, 1].argsort(0)
    xSort = xMat.copy()
    xSort.sort(0)
    yHat_list = list(yHat)
    fg = plt.figure()
    fg.clf()
    ax = fg.add_subplot(111)
    ySort = []
    for i in xInd:
        ySort.append(yHat_list[i])
    ax.plot(xSort[:,1], ySort)
    ax.scatter(xMat[:, 1].flatten().A[0], yMat[:, 0].flatten().A[0])
    plt.show()

def rssError(yArr, yHat):
    return ((yArr-yHat)**2).sum()

# ___________________岭回归______________
def ridgeRegress(xMat, yMat, lam = 0.2):
    xTx = xMat.T * xMat
    denom = xTx + lam * mat(eye(shape(xMat)[1]))
    if linalg.det(denom) == 0:
        print 'This changed matrix is singular, cannot do inverse'
        return
    wHat = denom.I * xMat.T * yMat
    return wHat

def testRidge(xArr, yArr):
    xMat = mat(xArr)
    yMat = mat(yArr)
    yMean = mean(yMat, 0)
    yMat = (yMat - yMean)/var(yMat, 0)
    xMean = mean(xMat, 0)
    xVar = var(xMat, 0)
    xMat = (xMat-xMean)/xVar
    numTestIter = 30
    wMat = mat(zeros((numTestIter, shape(xArr)[1])))
    for i in range(numTestIter):
        wMat[i, :] = ridgeRegress(xMat, yMat, exp(i - 10)).T
    return wMat

def stageWise(xArr, yArr, eps = 0.01, numIt = 100):
    xMat = mat(xArr)
    yMat = mat(yArr)
    m,n = shape(xMat)
    yMat = yMat - mean(yMat)
    xMat = (xMat - mean(xMat, 0))/var(xMat, 0)
    returnMat = mat(zeros((numIt, n)))
    ws = zeros((n, 1))
    ws_test = ws.copy()
    ws_max = ws.copy()
    for i in range(numIt):
        lowestError = inf
        for j in range(n):
            for sign in [1, -1]:
                ws_test = ws.copy()
                ws_test[j,0] += sign * eps
                y_test = xMat * ws_test
                rss = rssError(yMat.A, y_test.A)
                if rss < lowestError:
                    lowestError = rss
                    ws_max = ws_test
        ws = ws_max.copy()
        returnMat[i, :] = ws.T
        print ws.T
    return returnMat


# ______________EXAMPLE:LEGO_______________
def searchForSet(retX, retY, setNum, yr, numPce, origPrc):
    sleep(10)
    myAPIstr = 'get from code.google.com'
    searchURL = 'https://www.googleapis.com/shopping/search/v1/public/products?key=%s&country=US&q=lego+%d&alt=json' % (myAPIstr, setNum)
    page = urllib2.urlopen(searchURL)
    retDict = json.loads(pg.read())
    for i in range(len(retDict['items'])):
        try:
            currItem = retDict['items']['i']
            if currItem['product']['condition'] == 'new':
                newFlag = 1
            else:
                newFlag = 0
            listOfInv = currItem['product']['inventories']
            for item in listOfInv:
                sellingPrice = item['price']
                if sellingPrice > 0.5*origPrc:
                    print '%d\t%d\t%d\t%f\t%f' % (yr, numPce, newFlag, origPrc, sellingPrice)
                    retX.append([yr, numPce, newFlag, origPrc])
                    retY.append([sellingPrice])
        except:
            print 'problem with item %d' % i

def setDataCollect(retX, retY):
    searchForSet(retX, retY, 8288, 2006, 800, 49.99)
    searchForSet(retX, retY, 10030, 2002, 3096, 269.99)
    searchForSet(retX, retY, 10179, 2007, 5195, 499.99)
    searchForSet(retX, retY, 10181, 2007, 3428, 199.99)
    searchForSet(retX, retY, 10189, 2008, 5922, 299.99)
    searchForSet(retX, retY, 10196, 2009, 3263, 249.99)

if __name__ == '__main__':
    # 1
    # data, label = loadDataSet('ex0.txt')
    # ws = standRegress(data,label)
    # plotLR(data, label, ws)
    # yHat = data * ws
    # print corrcoef(yHat.T, mat(label).T)      #预测数据与真实数据的相关系数
    # print ws

    # 2
    # data, label = loadDataSet('ex0.txt')
    # yHat = testLwlr(data, data, label, 0.01)
    # plotLWLR(data, label, yHat)

    # 3
    # data, label = loadDataSet('abalone.txt')
    # yHat_01 = testLwlr(data[0:99], data[0:99], label[0:99], 0.1)
    # yHat_1 = testLwlr(data[0:99], data[0:99], label[0:99], 1)
    # yHat_10 = testLwlr(data[0:99], data[0:99], label[0:99], 10)
    # print 'the square error of training set is :\nk=0.1\t:\t%f \nk=1\t:\t%f \nk=10\t:\t%f' % (rssError(label[0:99], yHat_01), rssError(label[0:99], yHat_1), rssError(label[0:99], yHat_10))

    # yHat_01 = testLwlr(data[100:199], data[0:99], label[0:99], 0.1)
    # yHat_1 = testLwlr(data[100:199], data[0:99], label[0:99], 1)
    # yHat_10 = testLwlr(data[100:199], data[0:99], label[0:99], 10)
    # print 'the square error of test set is :\nk=0.1\t:\t%f \nk=1\t:\t%f \nk=10\t:\t%f' % (rssError(label[100:199], yHat_01), rssError(label[100:199], yHat_1), rssError(label[100:199], yHat_10))

    # 4
    # data, label = loadDataSet('abalone.txt')
    # ridge_weights = testRidge(data, label)
    # import matplotlib.pyplot as plt
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(ridge_weights)
    # plt.show()

    # 5
    # data, label = loadDataSet('abalone.txt')
    # print stageWise(data, label, eps = 0.001, numIt = 5000)

    # 6
    lgX = []
    lgY = []
    setDataCollect(lgX, lgY)
