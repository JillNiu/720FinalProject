import pandas as pd
import csv
# 5500
csvfile = pd.read_csv('RevProFile_sm.csv')
csvfile = csvfile[29500:35000]
csvfile = csvfile.values.tolist()

f = open('Rec_dataset.csv', 'w')
writer =csv.writer(f)
for i in csvfile:
    writer.writerow(i)
