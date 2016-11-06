#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lxm
# @Date:   2015-11-16 13:49:44
# @Last Modified by:   lxm
# @Last Modified time: 2015-11-16 16:25:27

class TreeNode:
    def __init__(self, nameValue,numOccur, parentNode):
        self.name=nameValue
        self.count=numOccur
        self.nodeLink=None
        self.parent=parentNode
        self.children={}

    def inc(self, numOccur):
        self.count+=numOccur

    def disp(self, ind=1):
        print "  "*ind, self.name,"  ",self.count
        for kid in self.children.values():
            kid.disp(ind+1)

def createTree(dataSet, minSup):
    headerTable={}
    for data in dataSet:
        for item in data:
            headerTable[item]=headerTable.get(item,0)+dataSet[data]
    for item in headerTable.keys():
        if headerTable[item]<minSup:
            del(headerTable[item])
    freqItemSet=set(headerTable.keys())
    if len(freqItemSet)==0:
        return None,None
    for k in headerTable.keys():
        headerTable[k]=[headerTable[k],None]
    retTree=TreeNode('Null Node', 1, None)
    for data,count in dataSet.items():
        localD={}
        for item in data:
            if item in freqItemSet:
                localD[item]=headerTable[item][0]
        if len(localD)>0:
            curSortData=[a[0] for a in sorted(localD.items(), key=lambda p:p[1], reverse=True)]
            updateTree(curSortData, retTree, headerTable, count)
    return retTree, headerTable

def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]]=TreeNode(items[0],count,inTree)
        if headerTable[items[0]][1]==None:
            headerTable[items[0]][1]=inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items)>1:
        updateTree(items[1:], inTree.children[items[0]], headerTable, count)

def updateHeader(firstNode, addNode):
    while firstNode.nodeLink is not None:
        firstNode=firstNode.nodeLink
    firstNode.nodeLink=addNode

def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

def ascendTree(leafNode,prefixPath):
    if leafNode.parent!=None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

def findPrefixPath(basePat, leafNode):
    condPats={}
    while leafNode is not None:
        prefixPath=[]
        ascendTree(leafNode, prefixPath)
        if len(prefixPath)>1:
            condPats[frozenset(prefixPath[1:])]=leafNode.count
        leafNode=leafNode.nodeLink
    return condPats

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]#(sort header table)
    for basePat in bigL:  #start from bottom of header table
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        #print 'finalFrequent Item: ',newFreqSet    #append to set
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        #print 'condPattBases :',basePat, condPattBases
        #2. construct cond FP-tree from cond. pattern base
        myCondTree, myHead = createTree(condPattBases, minSup)
        #print 'head from conditional tree: ', myHead
        if myHead != None: #3. mine cond. FP-tree
            #print 'conditional tree for: ',newFreqSet
            #myCondTree.disp(1)
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

if __name__ == '__main__':
    # 1
    # rootNode=TreeNode('first',10,None)
    # rootNode2=TreeNode('second',9,None)
    # rootNode.children['eye']=TreeNode('eye',8,None)
    # rootNode.disp()
    #
    # 2
    # simpDat = loadSimpDat()
    # dataSet = createInitSet(simpDat)
    # FPTree, headerTable = createTree(dataSet, 3)
    # FPTree.disp()
   # print headerTable

    # 3
    # simpDat = loadSimpDat()
    # dataSet = createInitSet(simpDat)
    # FPTree, headerTable = createTree(dataSet, 3)
    # freqItems=[]
    # mineTree(FPTree,headerTable,3,set([]),freqItems)

    # 4
    # simpDat = [line.strip().split() for line in open('kosarak.dat').readlines()]
    # dataSet = createInitSet(simpDat)
    # FPTree, headerTable=createTree(dataSet,100000)
    # freqItems=[]
    # mineTree(FPTree, headerTable,100000,set([]), freqItems)
    # print freqItems

    # 5
    import time
    t1 = time.time()
    data = ['MONKEY', 'DONKEY', 'MAKE', 'MUCKY', 'COOKIE']
    data = map(list, data)
    dataSet = createInitSet(data)
    FPTree, headerTable = createTree(dataSet, 3)
    freqItems = []
    mineTree(FPTree, headerTable, 3, set([]), freqItems)
    print time.time()-t1
    print freqItems
