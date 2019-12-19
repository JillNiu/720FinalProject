import csv
import pandas as pd
import sys, math, random, collections
from cffi.backend_ctypes import xrange

csvfile = open('file_classify.csv', 'r')
reader = csv.reader(csvfile)
filePath = []
lables = []
for i in reader:
    filePath.append(i)
# print(len(filePath))
# 6556

# 0-500 category: training data
filePath = filePath[0:500]
num = len(filePath)
for i in range(0,num):
    filePath[i].insert(0, str(i))
    lables.append('C'+str(i))

def generate_text():
    f_train = []
    for i in filePath:
        for j in i:
            f_train.append(j)
    print(len(f_train))
    # amount of file paths: 141624(500)
    f_train.append("404")


    # train data;
    temp = ''
    j = 0
    text = []
    tem_l = []
    for i in range(1, len(f_train)):
        if f_train[j].isdigit() == True and f_train[i].isdigit() == False:
            a = f_train[i].replace("/", ' ')
            temp += a
            tem_l.append(temp)

        elif f_train[i].isdigit() == True:
            text.append(tem_l)
            j = i
            temp = ''
            tem_l = []
    # print(text)
    trainText = []
    for i in range(0, len(text)):
        text[i].insert(0, 'C'+str(i))
        t = ' '.join(text[i])
        trainText.append(t)

    # print(trainText)
    return trainText

def lable2id(lable):
    for i in xrange(len(lables)):
        if lable == lables[i]:
            return i
    # raise Exception('Error lable %s' % (lable))

def doc_dict():

    return [0]*len(lables)
def mutual_info(N, Nij, Ni_, N_j):
    '''
        计算互信息，这里log的底取为2
    '''
    return Nij * 1.0 / N * math.log(N * (Nij + 1) * 1.0 / (Ni_ * N_j)) / math.log(2)

def count_for_cates(trainText):
    '''
        extract feature words
        compute the # of every word appeared in each class;
        the # of words in each class
    '''
    docCount = [0] * len(lables)
    wordCount = collections.defaultdict(doc_dict)
    # computation
    for line in trainText:
        lable, text = line.strip().split(' ', 1)
        index = lable2id(lable)
        words = text.split(' ')
        for word in words:
            wordCount[word][index] += 1
            docCount[index] += 1
    # print(docCount)
    # print(wordCount)

    # calculate mutual information
    miDict = collections.defaultdict(doc_dict)
    N = sum(docCount)
    for k, vs in wordCount.items():
        for i in xrange(len(vs)):
            N11 = vs[i]
            N10 = sum(vs) - N11
            N01 = docCount[i] - N11
            N00 = N - N11 - N10 - N01
            mi = mutual_info(N, N11, N10 + N11, N01 + N11) + mutual_info(N, N10, N10 + N11, N00 + N10) + mutual_info(N,
                                                                                                                     N01,
                                                                                                                     N01 + N11,
                                                                                                                     N01 + N00) + mutual_info(
                N, N00, N00 + N10, N00 + N01)
            miDict[k][i] = mi
    # print(miDict)

    f2 = open('featureFile.csv', 'w')
    writer2 = csv.writer(f2)
    writer2.writerow(docCount)
    fWords = set()
    for i in xrange(len(docCount)):
        keyf = lambda x: x[1][i]
        sortedDict = sorted(miDict.items(), key=keyf, reverse=True)
        # 10 * num of classes: num of featureWord
        for j in xrange(5*num):
            fWords.add(sortedDict[j][0])
    writer2.writerow(fWords)

def load_feature_words(featureFile):
    '''
        load docCounts(the # of words in each class) and feature words
    '''
    f = open(featureFile, 'r')
    r = csv.reader(f)
    temp = []
    for i in r:
        temp.append(i)
    docCounts = temp[0]
    features = temp[1]

    return docCounts,features

def train_bayes(trainText, featureFile):
    '''
        train naive bayes model
        compute the # of feature words appeared in each class
    '''
    docCounts, features = load_feature_words(featureFile)
    wordCount = collections.defaultdict(doc_dict)
    tCount = [0] * len(docCounts)
    for line in trainText:
        lable, text = line.strip().split(' ', 1)
        index = lable2id(lable)
        words = text.split(' ')
        for word in words:
            if word in features:
                tCount[index] += 1
                wordCount[word][index] += 1

    csvfile = open('modelFile.csv', 'w')
    outModel = csv.writer(csvfile)
    # Laplace Smoothing
    for k, v in wordCount.items():
        scores = [(v[i] + 1) * 1.0 / (tCount[i] + len(wordCount)) for i in xrange(len(v))]
        outModel.writerow([k , scores])


def main():
    trainText = generate_text()
    count_for_cates(trainText)
    train_bayes(trainText, 'featureFile.csv')

main()
