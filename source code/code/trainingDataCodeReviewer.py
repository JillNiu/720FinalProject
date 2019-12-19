import csv
import pandas as pd
import sys, math, random, collections
from cffi.backend_ctypes import xrange

# test data: 4600
def generate_text(f):

    temp = ''
    text = []
    for i in f:
        temp = i.replace("/", ' ')
        text.append(temp)

    # print(text)
    return text


def load_model(modelFile):
    '''
        从模型文件中导入计算好的贝叶斯模型
    '''
    f = open(modelFile, 'r')
    reader = csv.reader(f)
    scores = {}
    for line in reader:
        word, counts = line
        scores[word] = eval(counts)

    return scores

def load_feature_words(featureFile):
    '''
        从特征文件导入特征词
    '''
    f = open(featureFile, 'r')
    r = csv.reader(f)
    temp = []
    for i in r:
        temp.append(i)
    docCounts = temp[0]
    features = temp[1]
    # print(docCounts)
    # print(features)
    return docCounts,features

def predict(featureFile, modelFile, testText):
    '''
        预测文档的类标，标准输入每一行为一个文档
    '''
    docCounts, features = load_feature_words(featureFile)
    docCounts = list(map(int, docCounts))
    docScores = [math.log(count * 1.0 / sum(docCounts)) for count in docCounts]
    scores = load_model(modelFile)

    lable = []
    for line in testText:
        text = line.strip()
        words = text.split(' ')
        preValues = list(docScores)
        for word in words:
            if word in features:
                for i in xrange(len(preValues)):
                    preValues[i] += math.log(scores[word][i])
        m = max(preValues)
        pIndex = preValues.index(m)
        lable.append('C'+str(pIndex))
    # print(lable)
    return lable


def main():
    csvfile = pd.read_csv('Rec_dataset_shuffle.csv')
    # 5500 file
    fp = csvfile['filePath'][0:5000]
    fp = fp.values.tolist()

    testText = generate_text(fp)
    lable = predict('featureFile.csv', 'modelFile.csv', testText)

    rev = csvfile['reviewerId'][0:5000]
    rev = rev.values.tolist()
    reviewerId = []
    # 270 candidate(5000 file
    for i in rev:
        reviewerId.append(i)
    f = open('trainingData_CodeReviewer.csv', 'w')
    writer = csv.writer(f)
    header = ['reviewerId', 'filePathCategory']
    writer.writerow(header)
    for j in range(len(lable)):
        writer.writerow([reviewerId[j], lable[j]])
    print(len(set(reviewerId)))



    # for testing recommendation model
    fp2 = csvfile['filePath'][5000:5500]
    fp2 = fp2.values.tolist()
    # 500 file
    testText2 = generate_text(fp2)
    lable2 = predict('featureFile.csv', 'modelFile.csv', testText2)

    rev2 = csvfile['reviewerId'][5000:5500]
    rev2 = rev2.values.tolist()
    test_reviewer = []
    for j in rev2:
        test_reviewer.append(j)

    fnew = open('testingData_CodeReviewer.csv', 'w')
    writer2 = csv.writer(fnew)
    header = ['reviewerId', 'filePathCategory']
    writer2.writerow(header)
    for j in range(len(lable2)):
        writer2.writerow([test_reviewer[j], lable2[j]])

main()