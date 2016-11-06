#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lxm
# @Date:   2015-08-30 23:46:32
# @Last Modified by:   anchen
# @Last Modified time: 2015-09-05 23:24:41
from math import log
import operator
import treePlotter
import os
def calcShannonEnt(dataSet):
    data_len = len(dataSet)
    count = {}
    for i in range(data_len):
        label = dataSet[i][-1]
        count[label] = count.get(label, 0) + 1
    shannonEnt = 0.0
    for get_label in count:
        possibility = count[get_label] / float(data_len)
        shannonEnt -= possibility * log(possibility, 2)
    return shannonEnt


def splitDataSet(dataSet, specification, value):
    split_data = []
    for line_data in dataSet:
        # new_data = line_data[:]
        # if new_data[specification] == value:
        #     new_data.pop(specification)
        #     split_data.append(new_data)
        if line_data[specification] == value:
            new_data = line_data[:specification]
            new_data.extend(line_data[specification + 1:])
            split_data.append(new_data)
    return split_data


def chooseBestFeatureToSplit(dataSet):
    BestEnt = 0.0
    BestFeature = -1
    BaseEnt = calcShannonEnt(dataSet)
    data_num = len(dataSet)
    feature_num = len(dataSet[0]) - 1
    for i in range(feature_num):
        each_feature_num = set([k[i] for k in dataSet])
        Ent = 0.0
        for j in each_feature_num:
            split_data = splitDataSet(dataSet, i, j)
            prob = len(split_data) / float(len(dataSet))
            Ent += prob * calcShannonEnt(split_data)
        Total_Ent = BaseEnt - Ent
        if Total_Ent > BestEnt:
            BestEnt = Total_Ent
            BestFeature = i
    return BestFeature


def majorityCnt(classList):
    list_len = len(classList)
    count = {}
    for i in range(list_len):
        count[classList[i]] = count.get(classList[i], 0) + 1
    sortedcount = sorted(
        count.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedcount[0][0]


def createTree(dataSet, labels):
    new_label = labels[:]
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    best_class_choice = chooseBestFeatureToSplit(dataSet)
    best_label = new_label[best_class_choice]
    myTree = {best_label: {}}
    del(new_label[best_class_choice])
    best_class = set([example[best_class_choice] for example in dataSet])
    for sub_feature in best_class:
        sub_labels = new_label[:]
        split_sub_data = splitDataSet(dataSet, best_class_choice, sub_feature)
        myTree[best_label][sub_feature] = createTree(
            split_sub_data, sub_labels)
    return myTree


def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels


def classify(inputTree, featLabels, testVec):
    first_node = inputTree.keys()[0]
    second_floor = inputTree[first_node]
    first_feat = featLabels.index(first_node)
    for key in second_floor:
        if key == testVec[first_feat]:
            if type(second_floor[key]).__name__ == 'dict':
                classify_result = classify(
                    second_floor[key], featLabels, testVec)
            else:
                classify_result = second_floor[key]
    return classify_result

def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(inputTree, fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename)
    tree =  pickle.load(fr)
    fr.close()
    return tree


if __name__ == '__main__':
    # data, label = createDataSet()
    # if not os.path.exists('classifier_tree.txt'):
    #     myTree = createTree(data, label)
    #     storeTree(myTree, 'classifier_tree.txt')
    # else:
    #     myTree = grabTree('classifier_tree.txt')
    # print classify(myTree, label, [1,1])
    # treePlotter.createPlot(myTree)
    lensesLabel = ['age', 'prescript', 'astigmatic', 'tearRate']    #年龄，前科，散光，流泪量
    if not os.path.exists('lenses_tree.txt'):
        fr = open('lenses.txt')
        lenses = [inst.strip().split('\t') for inst in fr.readlines()]
        myTree = createTree(lenses, lensesLabel)
        storeTree(myTree, 'lenses_tree.txt')
        print myTree
    else:
        myTree = grabTree('lenses_tree.txt')
    treePlotter.createPlot(myTree)
