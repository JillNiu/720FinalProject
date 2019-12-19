import csv
import pandas as pd
class stringCompare:
    def path2List(self, fileString):
        return fileString.split("/")

    def LCP(self, f1, f2):
        f1 = self.path2List(f1)
        f2 = self.path2List(f2)
        common_path = 0
        min_length = min(len(f1), len(f2))
        for i in range(min_length):
            if f1[i] == f2[i]:
                common_path += 1
            else:
                break
        return common_path

    def LCSuff(self, f1, f2):
        f1 = self.path2List(f1)
        f2 = self.path2List(f2)
        common_path = 0
        r = range(min(len(f1), len(f2)))
        # r.reverse()
        for i in reversed(r):
            if f1[i] == f2[i]:
                common_path += 1
            else:
                break
        return common_path

    def LCSubstr(self, f1, f2):
        f1 = self.path2List(f1)
        f2 = self.path2List(f2)
        common_path = 0
        if len(set(f1) & set(f2)) > 0:
            mat = [[0 for x in range(len(f2) + 1)] for x in range(len(f1) + 1)]
            for i in range(len(f1) + 1):
                for j in range(len(f2) + 1):
                    if i == 0 or j == 0:
                        mat[i][j] = 0
                    elif f1[i - 1] == f2[j - 1]:
                        mat[i][j] = mat[i - 1][j - 1] + 1
                        common_path = max(common_path, mat[i][j])
                    else:
                        mat[i][j] = 0
        return common_path

    def LCSubseq(self, f1, f2):
        f1 = self.path2List(f1)
        f2 = self.path2List(f2)
        if len(set(f1) & set(f2)) > 0:
            L = [[0 for x in range(len(f2) + 1)] for x in range(len(f1) + 1)]
            for i in range(len(f1) + 1):
                for j in range(len(f2) + 1):
                    if i == 0 or j == 0:
                        L[i][j] = 0
                    elif f1[i - 1] == f2[j - 1]:
                        L[i][j] = L[i - 1][j - 1] + 1
                    else:
                        L[i][j] = max(L[i - 1][j], L[i][j - 1])
            common_path = L[len(f1)][len(f2)]
        else:
            common_path = 0
        return common_path

def similarityScore(f1, f2):
    strCompare = stringCompare()
    commonPath1 = strCompare.LCSubseq(f1, f2)
    commonPath2 = strCompare.LCSubstr(f1, f2)
    commonPath3 = strCompare.LCSuff(f1, f2)
    commonPath4 = strCompare.LCP(f1, f2)
    len_f1 = len(f1.split("/"))
    len_f2 = len(f2.split("/"))
    similarity1 = commonPath1 / max(len_f1, len_f2)
    similarity2 = commonPath2 / max(len_f1, len_f2)
    similarity3 = commonPath3 / max(len_f1, len_f2)
    similarity4 = commonPath4 / max(len_f1, len_f2)
    score = (similarity1+similarity2+similarity3+similarity4)/4
    return score

def main():
    csvfile = pd.read_csv('RevProFile_sm.csv')
    list1 = []
    f = open('file_classify.csv', 'w', newline='')
    writer = csv.writer(f)
    filePath = csvfile['filePath'][0:10000]
    filePath = list(set(filePath))
    for i in range(0, len(filePath)-1):
        temp = []
        f1 = filePath[i]
        temp.append(f1)
        for k in range(i+1, len(filePath)):
            f2 = filePath[k]
            score = similarityScore(f1, f2)
            if score > 0.5:
                temp.append(f2)
        list1.append(temp)
    # print(list1)
    for i in list1:
        writer.writerow(i)


main()