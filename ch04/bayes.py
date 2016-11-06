#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2015-08-31 21:26:21
# @Last Modified by:   anchen
# @Last Modified time: 2015-09-01 14:11:19

from numpy import *
import os


def createvocabList(dataSet):
    vocab = set()
    for lists in dataSet:
        vocab = set(lists) | vocab
    return list(vocab)


def setOfWords2Vec(vocabList, inputSet):
    dataList = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            dataList[vocabList.index(word)] = 1
        else:
            print '%s is not the word in the vocabrary list.' % word
    return dataList


def bagOfWords2VecMN(vocabList, inputSet):
    dataList = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            dataList[vocabList.index(word)] += 1
        else:
            # print '%s is not the word in the vocabrary list.' % word
            pass
    return dataList


def trainNB(trainMat, trainCat):
    doc_num = len(trainMat)
    word_num = len(trainMat[0])
    pc = sum(trainCat) / float(doc_num)
    p1vec = ones(word_num)
    p0vec = ones(word_num)
    p1sum = float(word_num)
    p0sum = float(word_num)
    for k in range(doc_num):
        if trainCat[k] == 1:
            p1vec += trainMat[k]
            p1sum += sum(trainMat[k])
        else:
            p0vec += trainMat[k]
            p0sum += sum(trainMat[k])
    p1Vect = log(p1vec / p1sum)
    p0Vect = log(p0vec / p0sum)
    return p0Vect, p1Vect, pc


def classifyNB(input_doc, p1vec, p0vec, pc):
    p1 = sum(array(input_doc) * p1vec) + log(pc)
    p0 = sum(array(input_doc) * p0vec) + log(1 - pc)
    if p1 > p0:
        return 1
    else:
        return 0


def classifyTest():
    list_of_words, class_vec = getdataSet()
    vocab_list = createvocabList(list_of_words)
    classlist = {0: 'I love dogs.', 1: 'I hate dogs!'}
    trainMat = []
    for postinDoc in list_of_words:
        trainMat.append(setOfWords2Vec(vocab_list, postinDoc))
    p0, p1, pc = trainNB(trainMat, class_vec)
    test_doc = [['love', 'my', 'dog'], [
        'love', 'cute', 'stupid', 'lxm', 'help', 'please']]
    test_word_list = setOfWords2Vec(vocab_list, test_doc[0])
    print 'the word %s is classified as : %s' % (test_doc[0], classlist[classifyNB(test_word_list, p1, p0, pc)])
    test_word_list = setOfWords2Vec(vocab_list, test_doc[1])
    print 'the word %s is classified as : %s' % (test_doc[1], classlist[classifyNB(test_word_list, p1, p0, pc)])


def textParse(text_string):
    import re
    list_of_tokens = re.split(r'\W*', text_string)
    return [word for word in list_of_tokens if len(word) > 2]


def spamTest():
    docList = []
    classList = []
    fullText = []
    for i in range(1, 26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        classList.append(0)
    vocab_list = createvocabList(docList)
    training_set = range(50)
    test_set = []
    for k in range(10):
        while True:
            index = int(random.uniform(0, len(training_set)))
            if index in test_set:
                continue
            else:
                test_set.append(index)
                break
    training_set = set(training_set) - set(test_set)
    training_set = list(training_set)
    trainMat = []
    train_data = []
    # test_data = []
    train_class = []
    for postinDoc in docList:
        trainMat.append(setOfWords2Vec(vocab_list, postinDoc))
    for k in training_set:
        train_data.append(trainMat[k])
        train_class.append(classList[k])
    # for k in test_set:
    #     test_data.append(trainMat[k])
    p0, p1, pc = trainNB(train_data, train_class)
    errorCount = 0
    print 'The VSM model is: ', vocab_list
    for k in test_set:
        guess = classifyNB(trainMat[k], p1, p0, pc)
        real = classList[k]
        print 'The Vector of each email:', trainMat[k]
        print 'The Truth:%d and The Guess:%d' % (int(guess), int(real))
        
    print 'the error rate is %f' % (errorCount / float(len(test_set)))



if __name__ == '__main__':
    # list_of_words, class_vec = getdataSet()
    # vocab_list = createvocabList(list_of_words)
    # trainMat = []
    # for postinDoc in list_of_words:
    #     trainMat.append(setOfWords2Vec(vocab_list, postinDoc))
    # p0, p1, pc = trainNB(trainMat, class_vec)
    # print p0
    # print p1
    # print pc
    spamTest()
    # if os.path.exists('feed1.txt') and os.path.exists('feed0.txt'):
    #     f1 = open('feed1.txt')
    #     f0 = open('feed0.txt')
    #     feed1 = pickle.load(f1)
    #     feed0 = pickle.load(f0)
    #     f1.close()
    #     f0.close()
    # else:
    #     feed1 = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
    #     feed0 = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
    #     f1 = open(r'feed1.txt', 'w+')
    #     f0 = open(r'feed0.txt', 'w+')
    #     pickle.dump(feed1, f1)
    #     pickle.dump(feed0, f0)
    #     f1.close()
    #     f0.close()
    # getTopWords(feed1, feed0)
    #vocabList, p1, p0 = localWords(feed1,feed0)
