#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lxm
# @Date:   2015-08-31 12:57:44
# @Last Modified by:   anchen
# @Last Modified time: 2015-08-31 17:45:59
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import decision_tree
decisionNode = dict(boxstyle='sawtooth', fc='0.8')
leafNode = dict(boxstyle='round4', fc='0.8')
arrow_args = dict(arrowstyle='<-')


def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
                            xytext=centerPt, textcoords='axes fraction',
                            va='center', ha='center', bbox=nodeType, arrowprops=arrow_args)


# def createPlot():
#     fig = plt.figure(1, facecolor='white')
#     fig.clf()
#     createPlot.ax1 = plt.subplot(111, frameon=False)
#     plotNode("Decision Node", (0.5, 0.1), (0.1, 0.5), decisionNode)
#     plotNode("Leaf Node", (0.8, 0.1), (0.3, 0.8), leafNode)
#     plt.show()

def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
    createPlot.ax1.text(
        xMid, yMid, txtString, va="center", ha="center", rotation=30)


# if the first key tells you what feat was split on
def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)  # this determines the x width of this tree
    depth = getTreeDepth(myTree)
    firstStr = myTree.keys()[0]  # the text label for this node should be this
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) /
              2.0 / plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    for key in secondDict.keys():
        # test to see if the nodes are dictonaires, if not they are leaf nodes
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], cntrPt, str(key))  # recursion
        else:  # it's a leaf node print the leaf node
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            plotNode(
                secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD
# if you do get a dictonary you know it's a tree, and the first element
# will be another dict


def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)  # no ticks
    # createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5 / plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()


def getNumLeafs(myTree):
    num_leafs = 0
    first_node = myTree.keys()[0]
    second_floor = myTree[first_node]
    for keys in second_floor:
        if type(second_floor[keys]).__name__ == 'dict':
            num_leafs += getNumLeafs(second_floor[keys])
        else:
            num_leafs += 1
    return num_leafs


def getTreeDepth(myTree):
    max_depth = 0
    now_depth = 0
    first_node = myTree.keys()[0]
    second_floor = myTree[first_node]
    for keys in second_floor:
        if type(second_floor[keys]).__name__ == 'dict':
            now_depth += getTreeDepth(second_floor[keys]) + 1
        else:
            now_depth = 1
        if now_depth > max_depth:
            max_depth = now_depth
    return max_depth


if __name__ == '__main__':
    data, label = decision_tree.createDataSet()
    myTree = decision_tree.createTree(data, label)
    print myTree
    print getNumLeafs(myTree)
    print getTreeDepth(myTree)
    createPlot(myTree)
