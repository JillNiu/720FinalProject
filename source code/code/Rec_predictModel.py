import csv
import pandas as pd
import sys, math, random, collections
from cffi.backend_ctypes import xrange

csvfile = pd.read_csv('trainingData_CodeReviewer.csv')
reviewerId = csvfile['reviewerId']
reviewerId = reviewerId.values.tolist()
lables = []
for i in reviewerId:
    if i not in lables:
        lables.append(i)
# 270 reviewers/lables
num = len(lables)
f = csvfile.values.tolist()
# print(f)
# print(lables)

def lable2id(lable):
    for i in xrange(len(lables)):
        if lable == lables[i]:
            return i

def doc_dict():

    return [0]*len(lables)

def mutual_info(N, Nij, Ni_, N_j):
    '''
        计算互信息，这里log的底取为2
    '''
    return Nij * 1.0 / N * math.log(N * (Nij + 1) * 1.0 / (Ni_ * N_j)) / math.log(2)

def count_for_cates(trainText):

    pplCount = [0] * len(lables)
    cateCount = collections.defaultdict(doc_dict)
    # computation
    for line in trainText:
        lable = line[0]
        fileCategory = line[1]
        index = lable2id(lable)
        # the # of one fileCategory reviewed by each ppl
        cateCount[fileCategory][index] += 1
        # the # of fileCategory reviewed by each ppl
        pplCount[index] += 1
    # print(pplCount)
    # print(cateCount)

    # calculate mutual information
    # the relevant degree of fileCategory to ppl
    miDict = collections.defaultdict(doc_dict)
    N = sum(pplCount)
    for k, vs in cateCount.items():
        for i in xrange(len(vs)):
            N11 = vs[i]
            N10 = sum(vs) - N11
            N01 = pplCount[i] - N11
            N00 = N - N11 - N10 - N01
            mi = mutual_info(N, N11, N10 + N11, N01 + N11) + mutual_info(N, N10, N10 + N11, N00 + N10) + mutual_info(N,
                                                                                                                     N01,
                                                                                                                     N01 + N11,
                                                                                                                     N01 + N00) + mutual_info(
                N, N00, N00 + N10, N00 + N01)
            miDict[k][i] = mi
    # print(miDict)

    f2 = open('Rec_featureFile.csv', 'w')
    writer2 = csv.writer(f2)
    writer2.writerow(pplCount)
    fWords = set()
    for i in xrange(len(pplCount)):
        keyf = lambda x: x[1][i]
        sortedDict = sorted(miDict.items(), key=keyf, reverse=True)
        # 10 * # of labels: # of most relevant fileCategory to ppl
        for j in xrange(30):
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
    pplCount = temp[0]
    features = temp[1]

    return pplCount,features

def train_bayes(trainText, featureFile):
    '''
        train naive bayes model
        compute the # of feature words appeared in each class
    '''
    pplCount, features = load_feature_words(featureFile)
    cateCount = collections.defaultdict(doc_dict)
    tCount = [0] * len(pplCount)
    for line in trainText:
        lable = line[0]
        fileCategory = line[1]
        index = lable2id(lable)
        if fileCategory in features:
            tCount[index] += 1
            cateCount[fileCategory][index] += 1

    csvfile = open('Rec_modelFile.csv', 'w')
    outModel = csv.writer(csvfile)
    # Laplace Smoothing
    for k, v in cateCount.items():
        scores = [(v[i] + 1) * 1.0 / (tCount[i] + len(cateCount)) for i in xrange(len(v))]
        outModel.writerow([k , scores])

def main():
    count_for_cates(f)
    train_bayes(f, 'Rec_featureFile.csv')

main()