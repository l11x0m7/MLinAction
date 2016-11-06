#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2015-09-05 11:09:42
# @Last Modified by:   anchen
# @Last Modified time: 2015-10-11 10:00:58
import random
from numpy import *
import time



def loadDataSet(filepath):                                          #加载数据
    fr = open(filepath)
    data_mat = []
    label_mat = []
    for line in fr.readlines():
        line = line.strip().split('\t')
        data_mat.append([float(line[0]), float(line[1])])
        label_mat.append([float(line[2])])
    return data_mat, label_mat


def selectJrand(i, m):                                              #SMO中随机选择j
    j = i
    while (j == i):
        j = int(random.uniform(0, m))
    return j


def clipAlpha(aj, H, L):                                            #对计算的aj进行修剪，保证a在[L,H]范围内
    if aj > H:
        aj = H
    if aj < L:
        aj = L
    return aj


# def smoSimple(dataIn, labelIn, C, toler, maxIter):
#     data = mat(dataIn)
#     label = mat(labelIn)
#     b = 0
#     m, n = shape(data)
#     iter = 0
#     alpha = mat(zeros((m, 1)))
#     while iter < maxIter:
#         alpha_change = 0
#         for i in range(m):
#             # print multiply(alpha,label.T).T
#             # print data * data[i, :].T
#             gxi = float(multiply(alpha, label).T * (data * data[i, :].T)) + b
#             Ei = gxi - float(label[i])
#             if ((label[i] * Ei < -toler and alpha[i] < C) or (label[i] * Ei > toler and alpha[i] > 0)):
#                 j = selectJrand(i, m)
#                 gxj = float(
#                     multiply(alpha, label).T * (data * data[j, :].T)) + b
#                 Ej = gxj - float(label[j])
#                 alpha_i_old = alpha[i].copy()
#                 alpha_j_old = alpha[j].copy()
#                 if(label[i] != label[j]):
#                     L = max(0, (alpha_j_old - alpha_i_old))
#                     H = min(C, (C + alpha_j_old - alpha_i_old))
#                 else:
#                     L = max(0, (alpha_j_old + alpha_i_old - C))
#                     H = min(C, (alpha_j_old + alpha_i_old))
#                 if L == H:
#                     print 'L = H.'
#                     continue
#                 eta = data[i, :] * data[i, :].T + data[j, :] * \
#                     data[j, :].T - 2.0 * data[i, :] * data[j, :].T
#                 if eta <= 0:
#                     print 'eta wrong.'
#                     continue
#                 alpha[j] = alpha[j] + label[j] * (Ei - Ej) / eta
#                 alpha[j] = clipAlpha(alpha[j], H, L)
#                 # alpha_j_unc = alpha_j_old + label[j]*(Ei-Ej)/eta
#                 # alpha_j_new = clipAlpha(alpha_j_unc, H, L)
#                 if (abs(alpha[j] - alpha_j_old) < 0.00001):
#                     print 'small change.'
#                     continue
#                 alpha[i] = alpha[i] + label[i] * \
#                     label[j] * (alpha_j_old - alpha[j])
#                 # alpha[i] = alpha_i_new
#                 # alpha[j] = alpha_j_new
#                 bi = -Ei - label[i] * data[i, :] * data[i, :].T * (alpha[i] - alpha_i_old) - label[
#                                                                  j] * data[j, :] * data[i, :].T * (alpha[j] - alpha_j_old) + b
#                 bj = -Ej - label[i] * data[i, :] * data[j, :].T * (alpha[i] - alpha_i_old) - label[
#                                                                  j] * data[j, :] * data[j, :].T * (alpha[j] - alpha_j_old) + b
#                 if (0 < alpha[i] < C and bi == bj):
#                     b = bi
#                 # elif(0<alpha[j]<C):
#                 #     b = bj
#                 else:
#                     b = (bi + bj) / 2.0
#                 alpha_change += 1
#                 print 'iter : %d, i : %d, pairs changed : %d' % (iter, i, alpha_change)
#         if alpha_change == 0:
#             iter += 1
#         else:
#             iter = 0
#         print 'iteration number is %d.' % iter
#     return alpha, b


def calcEk(oS, k):                                                                              #计算估计值与真实值的误差
    gxk = float(multiply(oS.alpha, oS.label).T * (oS.K[:, k])) + oS.b
    Ek = float(gxk - oS.label[k])
    return Ek


def selectJ(oS, i, Ei):                                                                         #通过选择与Ei差最大的Ej决定j
    max_j = -1
    max_deltaE = 0
    Ej = 0
    oS.ecache[i] = (1, Ei)
    valid_Ej = nonzero(oS.ecache[:, 0].A)[0]
    if len(valid_Ej) > 1:
        for k in valid_Ej:
            if k == i: continue
            Ek = calcEk(oS, k)
            deltaE = abs(Ek - Ei)
            if deltaE > max_deltaE:
                max_j = k
                max_deltaE = deltaE
                Ej = Ek
        return max_j, Ej
    else:
        j = selectJrand(i, oS.m)
        Ej = calcEk(oS, j)
        return j, Ej


def updataEk(oS, k):
    Ek = calcEk(oS, k)
    oS.ecache[k] = (1, Ek)


def innerL(oS, i):                                                                      #SMO内循环
    Ei = calcEk(oS, i)
    if ((oS.label[i] * Ei < -oS.toler and oS.alpha[i] < oS.C) or (oS.label[i] * Ei > oS.toler and oS.alpha[i] > 0)):
        j, Ej = selectJ(oS, i, Ei)
        alpha_i_old=oS.alpha[i].copy()
        alpha_j_old=oS.alpha[j].copy()
        if(oS.label[i] != oS.label[j]):
            L=max(0, (alpha_j_old - alpha_i_old))
            H=min(oS.C, (oS.C + alpha_j_old - alpha_i_old))
        else:
            L=max(0, (alpha_j_old + alpha_i_old - oS.C))
            H=min(oS.C, (alpha_j_old + alpha_i_old))
        if L == H:
            print 'L = H.'
            return 0
        eta=oS.data[i, :] * oS.data[i, :].T + oS.data[j, :] * oS.data[j, :].T - 2.0 * oS.data[i, :] * oS.data[j, :].T
        if eta <= 0:
            print 'eta wrong.'
            return 0
        oS.alpha[j]=oS.alpha[j] + oS.label[j] * (Ei - Ej) / eta
        oS.alpha[j]=clipAlpha(oS.alpha[j], H, L)
        updataEk(oS,j)
        if (abs(oS.alpha[j] - alpha_j_old) < 0.00001):
            print 'small change.'
            return 0
        oS.alpha[i]=oS.alpha[i] + oS.label[i] * oS.label[j] * (alpha_j_old - oS.alpha[j])
        updataEk(oS,i)
        bi=-Ei - oS.label[i] * oS.data[i, :] * oS.data[i, :].T * (oS.alpha[i] - alpha_i_old) - oS.label[j] * oS.data[j, :] * oS.data[i, :].T * (oS.alpha[j] - alpha_j_old) + oS.b
        bj=-Ej - oS.label[i] * oS.data[i, :] * oS.data[j, :].T * (oS.alpha[i] - alpha_i_old) - oS.label[j] * oS.data[j, :] * oS.data[j, :].T * (oS.alpha[j] - alpha_j_old) + oS.b
        if (0 < oS.alpha[i] < oS.C and bi == bj):
            oS.b=bi
        else:
            oS.b=(bi + bj) / 2.0
        return 1
    else:
        return 0




def smoP(dataIn, labelIn, C, toler, maxIter, kTup):                               #SMO算法
    oS = optStruct(mat(dataIn), mat(labelIn), C, toler, kTup)
    iter = 0
    entireSet = True
    alpha_change = 0
    while (iter < maxIter and (entireSet or alpha_change >0)):
        alpha_change = 0
        if entireSet:
            for i in range(oS.m):
                alpha_change += innerL(oS, i)
                print "fullset, iter : %d i : %d pairs changed %d" % (iter, i, alpha_change)
            iter += 1
        else:
            non_bound_points = nonzero(oS.ecache[:,0].A)[0]
            for i in non_bound_points:
                alpha_change += innerL(oS, i)
                print 'nonbound, iter : %d i : %d pairs changed %d' % (iter, i, alpha_change)
            iter += 1
        if entireSet :
            entireSet = False
        elif alpha_change == 0:
            entireSet = True
        print 'iteration number : %d' % iter
    return oS.alpha, oS.b



def calcW(alpha, dataIn, labelIn):
    data = mat(dataIn)
    label = mat(labelIn)
    w = 0
    m = shape(data)[0]
    for i in range(m):
        w += multiply(alpha[i]*label[i],data[i,:].T)
    return w

def getLabel(w, x, b):
    y = x * w + b
    return y

#-------------------------------------------------------------------Kernel Method（核方法）
def kernelTrans(dataIn, dataIn_i, kTup):                    #核转换
    m,n = shape(dataIn)
    K = mat(zeros((m, 1)))
    if kTup[0] == 'lin':
        K = dataIn * dataIn_i.T
    elif kTup[0] == 'rbf':
        for k in range(m):
            delta_data = dataIn[k,:] - dataIn_i
            K[k] = delta_data * delta_data.T
        K = exp(K/(-2*kTup[1]**2))
    else:
        raise NameError('The kernel you choose does not exist.')
    return K

class optStruct:                                                            #用于存储数据和参数的类

    def __init__(self, data, label, C, toler, kTup):
        self.data = data
        self.label = label
        self.C = C
        self.toler = toler
        self.b = 0
        self.m = shape(data)[0]
        self.n = shape(data)[1]
        self.alpha = mat(zeros((self.m, 1)))
        self.ecache = mat(zeros((self.m, 2)))
        self.K = mat(zeros((self.m, self.m)))
        for i in range(self.m):
            self.K[:,i] = kernelTrans(data, data[i,:], kTup)


def K_innerL(oS, i):                                                    #加入核函数的内循环
    Ei = calcEk(oS, i)
    if ((oS.label[i] * Ei < -oS.toler and oS.alpha[i] < oS.C) or (oS.label[i] * Ei > oS.toler and oS.alpha[i] > 0)):
        j, Ej = selectJ(oS, i, Ei)
        alpha_i_old=oS.alpha[i].copy()
        alpha_j_old=oS.alpha[j].copy()
        if(oS.label[i] != oS.label[j]):
            L=max(0, (alpha_j_old - alpha_i_old))
            H=min(oS.C, (oS.C + alpha_j_old - alpha_i_old))
        else:
            L=max(0, (alpha_j_old + alpha_i_old - oS.C))
            H=min(oS.C, (alpha_j_old + alpha_i_old))
        if L == H:
            print 'L = H.'
            return 0
        eta=oS.K[i, i] + oS.K[j, j] - 2.0 * oS.K[i, j]
        if eta <= 0:
            print 'eta wrong.'
            return 0
        oS.alpha[j]=oS.alpha[j] + oS.label[j] * (Ei - Ej) / eta
        oS.alpha[j]=clipAlpha(oS.alpha[j], H, L)
        updataEk(oS,j)
        if (abs(oS.alpha[j] - alpha_j_old) < 0.00001):
            print 'small change.'
            return 0
        oS.alpha[i]=oS.alpha[i] + oS.label[i] * oS.label[j] * (alpha_j_old - oS.alpha[j])
        updataEk(oS,i)
        bi=-Ei - oS.label[i] * oS.K[i, i] * (oS.alpha[i] - alpha_i_old) - oS.label[j] * oS.K[j, i] * (oS.alpha[j] - alpha_j_old) + oS.b
        bj=-Ej - oS.label[i] * oS.K[i, j] * (oS.alpha[i] - alpha_i_old) - oS.label[j] * oS.K[j, j] * (oS.alpha[j] - alpha_j_old) + oS.b
        if (0 < oS.alpha[i] < oS.C and bi == bj):
            oS.b=bi
        else:
            oS.b=(bi + bj) / 2.0
        return 1
    else:
        return 0

def K_smoP(dataIn, labelIn, C, toler, maxIter, kTup):                   #加入核函数的SMO算法
    oS = optStruct(mat(dataIn), mat(labelIn), C, toler, kTup)
    iter = 0
    entireSet = True
    alpha_change = 0
    while (iter < maxIter and (entireSet or alpha_change >0)):
        alpha_change = 0
        if entireSet:
            for i in range(oS.m):
                alpha_change += K_innerL(oS, i)
                print "fullset, iter : %d i : %d pairs changed %d" % (iter, i, alpha_change)
            iter += 1
        else:
            non_bound_points = nonzero(oS.ecache[:,0].A)[0]
            for i in non_bound_points:
                alpha_change += K_innerL(oS, i)
                print 'nonbound, iter : %d i : %d pairs changed %d' % (iter, i, alpha_change)
            iter += 1
        if entireSet :
            entireSet = False
        elif alpha_change == 0:
            entireSet = True
        print 'iteration number : %d' % iter
    return oS.alpha, oS.b

def testRBF(k1 = 1.3):
    data, label = loadDataSet(r'testSetRBF.txt')
    dataMat = mat(data)
    labelMat = mat(label)
    kTup = ('rbf', k1)
    alphas, b = K_smoP(data, label, 200, 0.0001, 100, kTup)
    sv_alpha = mat(alphas[alphas > 0]).T
    sv_num = nonzero(alphas.A>0)[0]
    sv_data = dataMat[sv_num]
    sv_label = labelMat[sv_num]
    print 'the number of support vectors is : %d ' % len(sv_num)
    m,n = shape(dataMat)
    errorCount = 0.0
    for i in range(m):
        K = kernelTrans(sv_data, dataMat[i,:], kTup)
        label_result =  K.T *multiply(sv_label, sv_alpha) + b
        if sign(label_result) != sign(labelMat[i]) :
            errorCount += 1
    print 'the training set\'s error rate is : %f' % (errorCount/m)

    data, label = loadDataSet(r'testSetRBF2.txt')
    dataMat = mat(data)
    labelMat = mat(label)
    m,n = shape(dataMat)
    errorCount = 0.0
    for i in range(m):
        K = kernelTrans(sv_data, dataMat[i,:], kTup)
        label_result =  K.T *multiply(sv_label, sv_alpha) + b
        if sign(label_result) != sign(labelMat[i]) :
            errorCount += 1
    print 'the test set\'s error rate is : %f' % (errorCount/m)

#-----------------------------------------------------SVM in Handwriting Digital Recognization（简单手写体识别）
def img2vector(filepath):
    fr = open(filepath)
    img = zeros((1,1024))
    for i in range(32):
        line = fr.readline()
        for j in range(32):
            img[0, i * 32 + j] = int(line[j])
    return img


def loadImage(dirName):
    from os import listdir
    trainingList = listdir(dirName)
    m = len(trainingList)
    data = zeros((m, 1024))
    label = []
    for i in range(m):
        file_name_all = trainingList[i]
        file_name = file_name_all.split('.')[0]
        number = int(file_name.split('_')[0])
        if number == 9 : label.append([-1])
        else : label.append([1])
        data[i,:] = img2vector('%s/%s' % (dirName, file_name_all))
    return data, label

def testDigits(kTup = ('rbf',100)):
    data, label = loadImage('trainingDigits')
    C = 200
    alphas, b = K_smoP(data, label, C, 0.0001, 10000, kTup)
    dataMat = mat(data)
    labelMat = mat(label)
    sv_alpha = mat(alphas[alphas > 0])
    sv_num = nonzero(alphas.A > 0)[0]
    sv_data = dataMat[sv_num]
    sv_label = labelMat[sv_num]
    print 'the number of support vectors is : %d ' % len(sv_num)
    m, n = shape(dataMat)
    errorCount = 0.0
    for i in range(m):
        K = kernelTrans(sv_data, dataMat[i, :], kTup)
        result = K.T * multiply(sv_label, sv_alpha.T) + b
        if sign(result) != sign(labelMat[i]):
            errorCount += 1
    print 'the error rate of training set is : %f ' % (errorCount/m)
    data, label = loadImage('testDigits')
    dataMat = mat(data)
    labelMat = mat(label)
    m, n = shape(dataMat)
    errorCount = 0.0
    for i in range(m):
        K = kernelTrans(sv_data, dataMat[i, :], kTup)
        result = K.T * multiply(sv_label, sv_alpha.T) + b
        if sign(result) != sign(label[i]):
            errorCount += 1
    print 'the error rate of test set is : %f' % (errorCount/m)

def handwritingResult(dataIn, labelIn, C, toler, maxIter, kTup):
    data, label = loadImage('trainingDigits')
    dataMat = mat(data)
    labelMat = mat(label)
    alphas, b = K_smoP(data, label, C, toler, maxIter, kTup)
    sv_alpha = mat(alphas[alphas > 0])
    sv_num = nonzero(alphas.A > 0)[0]
    sv_data = dataMat[sv_num]
    sv_label = labelMat[sv_num]
    dataMat = mat(dataIn)
    K = kernelTrans(sv_data, dataMat[0, :], kTup)
    result = K.T * multiply(sv_label, sv_alpha.T) + b
    real_result = sign(result)
    if real_result == -1 : real_result = 9
    print 'the training result is %d, and the real result is %d ' % (real_result, labelIn[0])


if __name__ == '__main__':
    # test1 无核函数的SVM测试
    # dataMat, labelMat = loadDataSet('testSet.txt')
    # alphas, b = smoP(dataMat, labelMat, 0.6, 0.001, 40, ('lin', 1.3))
    # w = calcW(alphas, dataMat, labelMat)
    # print 'the estimate value: %f' % getLabel(w, dataMat[99], b)[0][0]
    # print 'the real value: %f' % labelMat[99][0]

    # test2 测试高斯核函数
    testRBF(0.1)

    #test3 手写体识别测试（使用高斯核函数）
    # img = img2vector(r'9.txt')
    # label = [9]
    # handwritingResult(img, label, 200, 0.0001, 10000, ('rbf', 10))



