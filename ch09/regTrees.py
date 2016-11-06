#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2015-10-02 18:07:51
# @Last Modified by:   anchen
# @Last Modified time: 2015-10-06 16:40:43
from numpy import *
def loadDataSet(filename):
    dataMat = []
    fr = open(filename)
    for line in fr.readlines():
        line_list = map(float, (line.strip().split('\t')))
        dataMat.append(line_list)
    return dataMat

def binSplitDataSet(dataSet, feat, val):
    mat0 = dataSet[nonzero(dataSet[:,feat]>val)[0], :][0]
    mat1 = dataSet[nonzero(dataSet[:,feat]<=val)[0], :][0]
    return mat0, mat1

def linearSolve(dataSet):
    m, n = shape(dataSet)
    X = mat(ones((m,n)))
    Y = mat(ones((m,1)))
    X[:,1:n] = dataSet[:,0:n-1]
    Y = dataSet[:,-1]
    xTx = X.T * X
    if linalg.det(xTx) == 0:
        raise NameError('This matrix is singular, cannot do inverse,\ntry increasing the second value of ops')
    ws = xTx.I*(X.T*Y)
    return ws, X, Y

def regLeaf(dataSet):               #叶节点类型1-求输出的均值
    return mean(dataSet[:,-1])

def regErr(dataSet):                #误差表示1-求样本的输出的总平方误差和
    return var(dataSet[:,-1])*shape(dataSet)[0]

def modelLeaf(dataSet):              #叶节点类型2-节点为分段线性函数的斜率向量
    ws, X, Y = linearSolve(dataSet)
    return ws

def modelErr(dataSet):               #误差表示2-原数据与拟合曲线距离平方和
    ws, X, Y = linearSolve(dataSet)
    yHat = X * ws
    return sum(power(yHat-Y,2))

def chooseBestFeat(dataSet, leafType, errType, ops = (1,4)):
    tolS = ops[0]
    tolN = ops[1]
    if len(set(dataSet[:,-1].T.tolist()[0])) == 1 :return None, leafType(dataSet)
    m, n = shape(dataSet)
    S = errType(dataSet)
    best_feat = 0
    best_val = 0
    bestS = inf
    for feat_index in range(n-1):
        for split_val in set(dataSet[:,feat_index].T.tolist()[0]):
            mat0, mat1 = binSplitDataSet(dataSet,feat_index, split_val)
            if(shape(mat0)[0]<tolN or shape(mat1)[0]<tolN):continue
            newS = errType(mat0) + errType(mat1)
            if newS < bestS:
                best_feat = feat_index
                best_val = split_val
                bestS = newS
    if (S - bestS) < tolS:
                return None, leafType(dataSet)
    mat0, mat1 = binSplitDataSet(dataSet,feat_index, split_val)
    if(shape(mat0)[0]<tolN or shape(mat1)[0]<tolN):
        return None, leafType(dataSet)
    return best_feat, best_val

def createTree(dataSet, leafType=regLeaf, errType=regErr, ops=(1,4)):
    feat, val = chooseBestFeat(dataSet, leafType, errType, ops)
    if feat == None:    return val
    retTree = {}
    retTree['spInd'] = feat
    retTree['spVal'] = val
    lSet, rSet = binSplitDataSet(dataSet, feat, val)
    retTree['left'] = createTree(lSet, leafType, errType, ops)
    retTree['right'] = createTree(rSet, leafType, errType, ops)
    return retTree


def isTree(obj):
    return (type(obj).__name__ == 'dict')

def getMean(tree):
    if isTree(tree['left']):tree['left'] = getMean(tree['left'])
    if isTree(tree['right']):tree['right'] = getMean(tree['right'])
    return (tree['left'] + tree['right'])/2.0

def prune(tree, testData):
    if shape(testData)[0] == 0:
        return getMean(tree)
    if isTree(tree['left']) or isTree(tree['right']):
        ldat,rdat = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
    if isTree(tree['left']):
        tree['left'] = prune(tree['left'], ldat)
    if isTree(tree['right']):
        tree['right'] = prune(tree['right'], rdat)
    if not isTree(tree['left']) and not isTree(tree['right']):
        lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
        error_before_prune = sum(power(lSet[:,-1]-tree['left'],2)) + sum(power(rSet[:,-1]-tree['right'],2))
        tree_mean = (tree['left']+tree['right'])/2.0
        error_after_prune = sum(power(testData[:,-1]-tree_mean,2))
        if error_before_prune>error_after_prune:
            print "merging"
            return tree_mean
        else:
            return tree
    else:
        return tree

if __name__ == '__main__':
    # 1
    # testMat = mat(eye(4))
    # mat0, mat1=binSplitDataSet(testMat, 1, 0.5)
    # print mat0
    # print mat1

    # 2
    # myDat = loadDataSet('ex0.txt')
    # myMat = mat(myDat)
    # MyTree = createTree(myMat, regLeaf, regErr,(1,4))
    # print MyTree

    # 3
    # myDat1 = loadDataSet('ex2.txt')
    # myMat1 = mat(myDat1)
    # myTree = createTree(myMat1, ops = (0,1))
    # myDat2 = loadDataSet('ex2test.txt')
    # myMat2 = mat(myDat2)
    # print myTree
    # print prune(myTree, myMat2)

    # 4
    myDat1 = loadDataSet('exp2.txt')
    myMat1 = mat(myDat1)
    print createTree(myMat1, modelLeaf, modelErr,(1,10))
