import re

problem = '以下哪一个选项不属于家庭功能失调的范畴'
daan = '答案'
file = open('answer.txt','rb')
answers = ['A','B','C','D','√','×']
lines = file.readlines()
file.close()
for i in range(2638):
    words = str(lines[i].decode('utf-8'))
    if problem[2:-2]in words:
        print(words)
        break
while True :
    print(i)
    words = str(lines[i].decode('utf-8'))
    if daan in words :
        for j in words :
            if j in answers:
                print(j)
        break
    else:
        i += 1
