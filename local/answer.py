import re

problem = '全世界有（）大黑土地'
daan = '答案'
file = open('answer.txt','rb')
answers = ['A','B','C','D','√','×']
lines = file.readlines()
for i in range(len(lines)):
    words = str(lines[i].decode('utf-8'))
    if problem in words:
        print(words)
        break
while True :
    words = str(lines[i].decode('utf-8'))
    if daan in words :
        print(words)
        for j in words :
            if j in answers:
                print(j)
        break
    else:
        i += 1
file.close()