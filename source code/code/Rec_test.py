import csv
import pandas as pd
import sys, math, random, collections
from cffi.backend_ctypes import xrange

# test data: 500
csvfile = pd.read_csv('trainingData_CodeReviewer.csv')
reviewerId = csvfile['reviewerId']
reviewerId = reviewerId.values.tolist()
lables = []
for i in reviewerId:
    if i not in lables:
        lables.append(i)

def load_model(modelFile):

    f = open(modelFile, 'r')
    reader = csv.reader(f)
    scores = {}
    for line in reader:
        fileCategory, counts = line
        scores[fileCategory] = eval(counts)

    return scores

def load_feature_words(featureFile):

    f = open(featureFile, 'r')
    r = csv.reader(f)
    temp = []
    for i in r:
        temp.append(i)
    pplCount = temp[0]
    features = temp[1]
    # print(docCounts)
    # print(features)
    return pplCount,features

def lable2id(lable):
    for i in xrange(len(lables)):
        if lable == lables[i]:
            return i

def predict(featureFile, modelFile, testText):

    pplCount, features = load_feature_words(featureFile)
    pplCount = list(map(int, pplCount))
    pplScores = [math.log(count * 1.0 / sum(pplCount)) for count in pplCount]
    scores = load_model(modelFile)
    rCount = 0
    totCount = 0
    lable = []
    for line in testText:
        lable = line[0]
        fileCategory = line[1]
        index = lable2id(lable)
        preValues = list(pplScores)
        if fileCategory in features:
            for i in xrange(len(preValues)):
                preValues[i] += math.log(scores[fileCategory][i])
        m = max(preValues)
        pIndex = preValues.index(m)
        if pIndex == index:
            rCount += 1
        totCount += 1



def main():
    csvfile = pd.read_csv('testingData_CodeReviewer.csv')
    f1 = csvfile
    test_file = f1.values.tolist()
    predict('featureFile.csv', 'modelFile.csv', test_file)

main()