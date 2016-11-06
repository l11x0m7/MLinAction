#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lxm
# @Date:   2015-11-12 16:34:51
# @Last Modified by:   lxm
# @Last Modified time: 2015-11-15 19:39:49

import json

def loadDataSet():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]

def createC1(dataSet):
    C1=[]
    for line in dataSet:
        for item in line:
            if [item] not in C1:
                C1.append([item])
    return map(frozenset, C1)

def scanD(D,Ck,minSupport):     #change Ck to Lk
    support={}
    for data in D:
        for can in Ck:
            if can.issubset(data):
                if not support.has_key(can):
                    support[can]=1
                else:
                    support[can]+=1
    data_len=float(len(D))
    retData=[]
    supportRate={}
    for can in support:
        rate = support[can]/data_len
        if rate>=minSupport:
            retData.insert(0,can)
            supportRate[can]=rate
    return retData, supportRate

def createCk(Lk, k):
    Ck=[]
    length=len(Lk)
    for i in range(length):
        for j in range(i+1,length):
            L1=list(Lk[i])[:k-2]
            L2=list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1==L2:
                Ck.append((Lk[i]|Lk[j]))
    return Ck

def apriori(dataSet, minSupport=0.5):
    C1=createC1(dataSet)
    D=map(set, dataSet)
    L1, supportRate=scanD(D,C1,minSupport)
    L=[]
    L.append(L1)
    k=2
    while len(L[k-2])>2:
        Ck=createCk(L[k-2], k)
        Lk, Ratek=scanD(D,Ck,minSupport)
        L.append(Lk)
        supportRate.update(Ratek)
        k+=1
    return L, supportRate

def generateRules(L, supportRate, minConf=0.5):
    bigRuleList = []
    length=len(L)
    for i in range(1,length):
        for freqSet in L[i]:
            H1=[frozenset([item]) for item in freqSet]
            if i>1:
                rulesFromConseq(freqSet, H1, supportRate, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportRate, bigRuleList, minConf)
    return bigRuleList

def calcConf(freqSet, H1, supportRate, bigRuleList, minConf):
    prunedH = []
    for conseq in H1:
        conf = supportRate[freqSet]/supportRate[freqSet-conseq]
        if conf>=minConf:
            print freqSet-conseq, "---->", conseq, ":", json.dumps([supportRate[freqSet], conf])
            bigRuleList.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq)
    return prunedH

def rulesFromConseq(freqSet, H1, supportRate, bigRuleList, minConf):
    length=len(H1[0])
    if len(freqSet)>length+1:
        newH=createCk(H1,length+1)
        newH=calcConf(freqSet, newH, supportRate, bigRuleList, minConf)
        if len(newH)>1:
            rulesFromConseq(freqSet, newH, supportRate, bigRuleList, minConf)

if __name__ == '__main__':
    # 1
    # data = loadDataSet()
    # C1=createC1(data)
    # D=map(set, data)
    # print D
    # print C1
    # retData, supportRate=scanD(D,C1,0.5)
    # print retData
    # print supportRate

    # 2
    # data = loadDataSet()
    # L, supportRate = apriori(data, 0.7)
    # print L
    # print supportRate

    # 3
    # data = loadDataSet()
    # L, supportRate = apriori(data)
    # rule = generateRules(L,supportRate)
    # print rule

    # 4
    # mushDataSet = [map(int,(line.strip().split())) for line in open('mushroom.dat')]
    # L, supportRate =apriori(mushDataSet, 0.7)
    # print L[1]

    # 5
    # data = ['MONKEY', 'DONKEY', 'MAKE', 'MUCKY', 'COOKIE']
    # data = map(list, data)
    # L, supportRate = apriori(data, 0.6)
    # # print supportRate
    # rule = generateRules(L, supportRate, 0.8)
    # print rule


    # 6
    # data = [['Carb', 'Milk', 'Cheese', 'Bread'], 
    # ['Cheese', 'Milk', 'Apple', 'Pie', 'Bread'],
    # ['Apple', 'Milk', 'Bread', 'Pie'],
    # ['Bread', 'Milk', 'Cheese']]

    # L, supportRate = apriori(data, 0.6)
    # print L
    # rule = generateRules(L, supportRate, 0.8)
    # print rule

    # 7
    data = [['Kings', 'Sunset', 'Dairyland', 'Best'],
    ['Best', 'Dairyland', 'Goldenfarm', 'Tasty', 'Wonder'],
    ['Westcoast', 'Dairyland', 'Wonder', 'Tasty'], 
    ['Wonder', 'Sunset', 'Dairyland']]
    data2 = [['Carb', 'Milk', 'Cheese', 'Bread'], 
    ['Cheese', 'Milk', 'Apple', 'Pie', 'Bread'],
    ['Apple', 'Milk', 'Bread', 'Pie'],
    ['Bread', 'Milk', 'Cheese']]

    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] += data2[i][j]
    print data

    L, supportRate = apriori(data, 0.6)
    print L
    rule = generateRules(L, supportRate, 0.8)
    print rule
































