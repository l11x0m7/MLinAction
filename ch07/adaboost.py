#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2015-09-25 17:29:13
# @Last Modified by:   anchen
# @Last Modified time: 2015-09-30 21:02:44
from numpy import *
import matplotlib

def loadSimpData():
    dataMat = matrix([[1., 2.1], [2., 1.1], [1.3, 1.], [1., 1.], [2., 1.]])
    classLabel = matrix([[1.0], [1.0], [-1.0], [-1.0], [1.0]])
    return dataMat, classLabel

def stumpClassify(dataMat, dimen, var, symbol):
    m = shape(dataMat)[0]
    predict_label = mat(ones((m,1)))
    #for i in range(m):
    if symbol == 'lt':
        predict_label[dataMat[:, dimen] <= var] = -1.0
    else:
        predict_label[dataMat[:, dimen] > var] = -1.0
    return predict_label

def buildStump(data, label, D):
    dataMat = mat(data)
    labelMat = mat(label)
    m,n = shape(dataMat)
    min_err = inf
    step_num = 10.0
    best_class_label = mat(zeros((m, 1)))
    best_stump = {}
    for i in range(n):
        dimen_max = dataMat[:, i].max()
        dimen_min = dataMat[:, i].min()
        step = (dimen_max-dimen_min)/step_num
        for j in range(-1, int(step_num)+1):
            for inequal in ['lt', 'gt']:
                var = dimen_min + step * float(j)
                label = stumpClassify(dataMat, i, var, inequal)
                err_arr = mat(ones((m, 1)))
                err_arr[label == labelMat] = 0
                weighted_error = D.T * err_arr
                # print 'split: dimen%d, thresh: %.2f, thresh inequal: %s,the weighted error is %.3f' % (i, var, inequal, weighted_error)
                if weighted_error < min_err:
                    min_err = weighted_error
                    best_class_label = label.copy()
                    best_stump['dimen'] = i
                    best_stump['var'] = var
                    best_stump['inequal'] = inequal
    # print 'BEST______split: dimen%d, thresh: %.2f, thresh inequal: %s,the weighted error is %.3f' % \
    #                                                                        (best_stump['dimen'], best_stump['var'], best_stump['inequal'], min_err)
    return best_stump, best_class_label, min_err

def adaBoostTrainDS(data, label, numIt = 40):
    weak_classifier = []
    m = shape(data)[0]
    D = mat(ones((m, 1))/m)
    agg_class_est = mat(zeros((m, 1)))
    for i in range(numIt):
        weak_stump, weak_label, weak_err = buildStump(data, label, D)
        #print 'D: ', D.T
        #print 'Classifying Result:', weak_label.T
        alpha = float((log((1.0-weak_err)/max(1e-16, weak_err)))/2.0)
        weak_stump['alpha'] = alpha
        weak_classifier.append(weak_stump)
        expon = multiply(-1*alpha * mat(label), weak_label)
        Z = multiply(D, exp(expon))
        D = Z/Z.sum()
        agg_class_est += alpha * weak_label
        #print 'AggClassEst:', agg_class_est.T
        error_label = mat(zeros((m, 1)))
        error_label[mat(label) != mat(sign(agg_class_est))] = 1
        error_rate = float(error_label.T * mat(ones((m, 1)))/m)
        print 'total error: %f' % error_rate
        if error_rate == 0.0:break
    return weak_classifier, agg_class_est

def adaClassify(data, classifier):
    dataMat = mat(data)
    m = shape(data)[0]
    predict_label = mat(zeros((m,1)))
    for i in range(len(classifier)):
        sub_predict = stumpClassify(dataMat, classifier[i]['dimen'], classifier[i]['var'],classifier[i]['inequal'])
        predict_label += classifier[i]['alpha'] * sub_predict
        #print predict_label
    return sign(predict_label)

def loadDataSet(filepath):
    fr = open(filepath)
    dataMat = []
    labelMat = []
    line_num = len(fr.readline().strip().split('\t'))
    for line in fr.readlines():
        line_data = []
        lineArr = line.strip().split('\t')
        for i in range(line_num - 1):
            line_data.append(float(lineArr[i]))
        dataMat.append(line_data)
        labelMat.append(float(lineArr[-1]))
    fr.close()
    return mat(dataMat), mat(labelMat).transpose()


def plotROC(preStrengths, classLabel):
    import matplotlib.pyplot as plt
    cur = (1.0, 1.0)
    ySum = 0.0
    pos_class_num = sum(array(classLabel) == 1.0)
    ystep = 1/float(pos_class_num)
    xstep = 1/float(len(classLabel) - pos_class_num)
    sorted_indicies = preStrengths.argsort()
    fig = plt.figure()
    fig.clf()
    ax = plt.subplot(111)
    for index in sorted_indicies.tolist()[0]:
        if classLabel[index] == 1.0:
            delX = 0.0
            delY = ystep
        else:
            delX = xstep
            delY = 0.0
            ySum += cur[1]
        ax.plot([cur[0], cur[0]-delX], [cur[1], cur[1]-delY], c='r')
        cur = [cur[0]-delX, cur[1]-delY]
    ax.plot([0,1],[0,1],'b--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC curve')
    ax.axis([0,1,0,1])
    plt.show()
    AUC = ySum * xstep
    print 'AUC=%f' % AUC




if __name__ == '__main__':
    # 1
    # dataMat, labelMat = loadSimpData()
    # D = mat(ones((5,1))/5)
    # buildStump(dataMat, labelMat, D)

    # 2
    # dataMat, labelMat = loadSimpData()
    # Classifier = adaBoostTrainDS(dataMat, labelMat,9)
    # print Classifier

    # 3
    # dataMat, labelMat = loadSimpData()
    # Classifier = adaBoostTrainDS(dataMat, labelMat, 9)
    # result = adaClassify([[0,0], [5, 5]], Classifier)
    # print result

    # 4
    # dataMat, labelMat = loadDataSet('horseColicTraining2.txt')
    # testdata,testlabel = loadDataSet('horseColicTest2.txt')
    # Classifier = adaBoostTrainDS(dataMat, labelMat, 50)
    # result = adaClassify(testdata, Classifier)
    # m = shape(testdata)[0]
    # error_rate = 0.0
    # err_num  = multiply(result != testlabel , ones((m, 1))).sum()
    # error_rate = err_num/float(m)
    # print 'test error rate is : %f' % (error_rate)

    # 5
    dataMat, labelMat = loadDataSet('horseColicTraining2.txt')
    Classifier, agg_class_est = adaBoostTrainDS(dataMat, labelMat, 10)
    plotROC(agg_class_est.T, labelMat)
