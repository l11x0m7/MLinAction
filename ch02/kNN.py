#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lxm
# @Date:   2015-08-30 13:43:00
# @Last Modified by:   anchen
# @Last Modified time: 2015-08-31 13:04:03

from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt
from os import listdir


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    lables = ['A', 'A', 'B', 'B']
    return group, lables


def img2vector(pathname):
    fr = open(pathname)
    img_vec = zeros((1, 1024))
    for i in range(32):
        line = fr.readline()
        for j in range(32):
            img_vec[0, i * 32 + j] = int(line[j])
    return img_vec


def file2matrix(pathname):
    fr = open(pathname)
    arrayLines = fr.readlines()
    LineNum = len(arrayLines)
    returnMat = zeros([LineNum, 3])
    label_str2num = {'largeDoses': 3, 'smallDoses': 2, 'didntLike': 1}
    classLabelVector = []
    index = 0
    for line in arrayLines:
        line = line.strip()
        list_from_line = line.split('\t')
        returnMat[index, :] = list_from_line[0:3]
        classLabelVector.append(label_str2num[list_from_line[-1]])
        index += 1
    return returnMat, classLabelVector


def classify0(inX, dataSet, lables, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = lables[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(
        classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = (dataSet - tile(minVals, (m, 1))) / tile(ranges, (m, 1))
    return normDataSet, ranges, minVals


def datingClassTest():
    hoRatio = 0.10
    errorCount = 0.0
    dating_data_mat, dating_labels = file2matrix('datingTestSet.txt')
    norm_data_mat, ranges, minvals = autoNorm(dating_data_mat)
    m = norm_data_mat.shape[0]
    test_m = int(m * hoRatio)
    for i in range(test_m):
        classify_result = classify0(
            norm_data_mat[i, :], norm_data_mat[test_m: m, :],
            dating_labels[test_m: m], 3)
        print 'The classify type is %s, and the real answer is %s ' \
            % (classify_result, dating_labels[i])
        if classify_result != dating_labels[i]:
            errorCount += 1.0
    print 'the total error rate is : %f' % (errorCount / (float(test_m)))


def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    ffMiles = float(raw_input('frequent flier miles earned per year?\n'))
    percentTats = float(
        raw_input('percentage of time spent on the computer game?\n'))
    iceCream = float(raw_input('liters of ice cream consumed per year?\n'))
    dating_data_mat, dating_labels = file2matrix('datingTestSet.txt')
    norm_data_mat, ranges, minvals = autoNorm(dating_data_mat)
    input_data = array([ffMiles, percentTats, iceCream])
    input_data = (input_data - minvals) / ranges
    classify_result = classify0(input_data, norm_data_mat, dating_labels, 3)
    print 'you will like this person', resultList[classify_result - 1]


def handwritingTest():
    training_label = []
    training_data = listdir('trainingDigits')
    test_data = listdir('testDigits')
    training_len = len(training_data)
    test_len = len(test_data)
    training_vec = zeros((training_len, 1024))
    # test_vec = zeros((1, 1024))
    errorCount = 0.0
    for i in range(training_len):
        training_name = training_data[i]
        training_result = int(training_name.split('.')[0].split('_')[0])
        training_label.append(training_result)
        training_vec[i, :] = img2vector('trainingDigits/%s' % training_name)
    for i in range(test_len):
        test_name = test_data[i]
        test_result = int(test_name.split('.')[0].split('_')[0])
        test_vec = img2vector('testDigits/%s' % test_name)
        classify_result = classify0(test_vec, training_vec, training_label, 3)
        if classify_result != test_result:
            errorCount += 1.0
            print 'the classified result is', classify_result, \
                ', but the real answer is', test_result
    print 'the error rate is %f' % (errorCount / (float(test_len)))

if __name__ == '__main__':
    # data_mat, label = file2matrix(r'F:\datingTestSet.txt')
    # fig = plt.figure()
    # ax = fig.add_subplot(1,1,1)
    # ax.scatter(data_mat[:,0], data_mat[:, 1], 15*array(label), 20*array(label))
    # plt.show()
    # print classify0([0.5,0.6], group, lables, 3)
    # classifyPerson()
    # getvec = img2vector(r'F:\testDigits\0_13.txt')
    # print getvec[0,1:31]
    handwritingTest()
