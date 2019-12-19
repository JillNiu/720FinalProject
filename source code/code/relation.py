import csv
import json
data_filtered = json.load(open("data_filtered.json"))

# f = open('ReviewerProjectFile.csv', 'w', newline='')
# writer = csv.writer(f)
# head = ['reviewerId', 'projectName', 'filePath']
# writer.writerow(head)
result = []
for i in range(len(data_filtered)):
    messages = data_filtered[i]["messages"]
    revisions = data_filtered[i]["revisions"]
    ppl_list = []
    list_file = []
    list_project = []

    if 'project' in data_filtered[i]:
        projectName = data_filtered[i]['project']
        for j in range(len(messages)):
            if "author" in messages[j]:
                author = messages[j]["author"]
                if "_account_id" in author:
                    ppl = author["_account_id"]
                    # ppl_list.append(ppl)
                    for k, v in revisions.items():
                        if "files" in v:
                            file_path = v["files"].keys()
                            for j in file_path:
                                # list_file.append(j)
                                result.append([ppl, projectName, j])
# for i in range(len(result)):
#     writer.writerow(result[i])
# print(len(result))
# 15672576

result_sm = []
f2 = open('RevProFile_sm.csv', 'w', newline='')
writer2 = csv.writer(f2)
head = ['reviewerId', 'projectName', 'filePath']
writer2.writerow(head)
# 260702 unrepeat in 1000000
for i in result[0:1000000]:
    if i not in result_sm:
        result_sm.append(i)
print(len(result_sm))
for i in range(len(result_sm)):
    writer2.writerow(result_sm[i])


