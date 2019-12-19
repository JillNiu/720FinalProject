import json
import csv
# 51724 - 41943
data = json.load(open("aosp.json"))
print(len(data))

list1=[]
for i in range(len(data)):
    if data[i]["status"] != "NEW":
        temp = data[i]
        list1.append(temp)
print(len(list1))

jsobj = json.dumps(list1)
f = open("data_filtered.json", "w")
f.write(jsobj)
f.close()




