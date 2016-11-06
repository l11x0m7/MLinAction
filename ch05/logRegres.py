#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2015-09-01 14:16:16
# @Last Modified by:   anchen
# @Last Modified time: 2015-09-01 23:21:20
from numpy import *


def loadDataSet():
    data_set = []
    label_set = []
    fr = open('testSet.txt')
    text = fr.readlines()
    for line in text:
        line = line.strip().split('\t')
        data_set.append([1.0, float(line[0]), float(line[1])])
        label_set.append(int(line[2]))
    return data_set, label_set


def sigmoid(inX):
    return 1.0 / (1 + exp(-inX))


def gradAscent(dataMatIn, classLabels):
    data_mat = mat(dataMatIn)
    label_mat = mat(classLabels).transpose()
    m, n = shape(data_mat)
    alpha = 0.001
    max_circle_time = 500
    theta = ones((n, 1))
    for i in range(max_circle_time):
        h = sigmoid(data_mat * mat(theta))
        error = h - label_mat
        theta -= alpha * data_mat.transpose() * mat(error)
    return theta


def plotBestFit(theta):
    import matplotlib.pyplot as plt
    xcord1 = []
    ycord1 = []
    xcord0 = []
    ycord0 = []
    data_set, label_set = loadDataSet()
    data_num = shape(data_set)[0]
    for k in range(data_num):
        if label_set[k] == 1:
            xcord1.append(data_set[k][1])
            ycord1.append(data_set[k][2])
        else:
            xcord0.append(data_set[k][1])
            ycord0.append(data_set[k][2])
    fg = plt.figure()
    ax = fg.add_subplot(111)
    ax.scatter(xcord1, ycord1, c='red', s=30, marker='s')
    ax.scatter(xcord0, ycord0, c='green', s=30)
    x = arange(-3.0, 3.0, 0.1)
    y = (-theta[0] - theta[1] * x) / theta[2]
    plt.plot(x, y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()



# def randGradAscent(dataMat, classLabel, maxIter=150):
#     data_mat = mat(dataMat)  # 100*3
#     class_label = mat(classLabel).transpose()  # 100*1
#     m, n = shape(data_mat)
#     theta = ones((n, 1))  # 3*1
#     for i in range(maxIter):
#         data_index = range(m)
#         for k in range(m):
#             alpha = (4.0 / (i + k + 1.0) + 0.0001)
#             random_index = int(random.uniform(0, len(data_index)))
#             h = sigmoid(float((data_mat[random_index]) * theta))
#             error = h - class_label[random_index]
#             theta -= alpha * data_mat[random_index].transpose() * error
#             del data_index[random_index]
#     return theta

def randGradAscent(dataMatrix, classLabels, numIter=150):
    m,n = shape(dataMatrix)
    theta = ones((n, 1))   #initialize to all ones
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            alpha = 5/(1.0+j+i)+0.0001    #apha decreases with iteration, does not
            randIndex = int(random.uniform(0,len(dataIndex)))#go to 0 because of the constant
            h = sigmoid(sum(dataMatrix[randIndex]*theta))
            error = classLabels[randIndex] - h
            theta = theta + alpha * error * dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return theta

def classifyVector(inX, theta):
    # in_x = mat(inX)
    # theta_mat = mat(theta)
    # h = in_x * theta_mat
    h = sum(inX * theta)
    p = sigmoid(h)
    if p >0.5 :
        return 1.0
    else:
        return 0.0

def colicTest():
    fr_train = open('horseColicTraining.txt')
    fr_test = open('horseColicTest.txt')
    training_set = []
    training_label = []
    errorCount = 0.0
    test_num = 0.0
    for train_data in fr_train.readlines():
        train_data = train_data.strip().split('\t')
        training_set.append([float(x) for x in train_data[:-2]])
        training_label.append(float(train_data[-1]))
    theta = randGradAscent(array(training_set), training_label, 100)
    for test_data in fr_test.readlines():
        test_num += 1.0
        test_data = test_data.strip().split('\t')
        if classifyVector([float(x) for x in test_data[:-2]], theta) != float(test_data[-1]) :
            errorCount += 1.0
    error_rate = (errorCount / test_num)
    print 'the error rate is %f' % error_rate
    return error_rate

def multiTest():
    num = 10
    errorSum = 0.0
    for k in range(num):
        errorSum += colicTest()
    print 'the average iteration error rate is %f' % (errorSum/float(num))

if __name__ == '__main__':
    # dataArr, labelMat = loadDataSet()
    # theta = randGradAscent(dataArr, labelMat, 20)
    # plotBestFit(theta)
    # theta = gradAscent(dataArr, labelMat)
    # plotBestFit(theta)
    multiTest()
