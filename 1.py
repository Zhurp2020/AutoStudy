from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

username,password = input('用户名 密码').split()

daan = '答案'
file = open('answer.txt','rb')
answers = ['A','B','C','D','√','×']
lines = file.readlines()


findpro = re.compile(r'】.*?（')

driver = webdriver.Chrome()
driver.get("http://www.elearning.shu.edu.cn/portal")

loginbutton = driver.find_element_by_css_selector('.loginSub')

loginaction = webdriver.ActionChains(driver)
loginaction.click(loginbutton)
loginaction.perform()

userin = driver.find_element_by_name('username')
pwdin = driver.find_element_by_name('password')
submit = driver.find_element_by_name('login_submit')

inputaction = webdriver.ActionChains(driver)
inputaction.click(userin)
inputaction.send_keys_to_element(userin,username)
inputaction.click(pwdin)
inputaction.send_keys_to_element(pwdin,password)
inputaction.click(submit)
inputaction.perform()

driver.get('http://mooc1.elearning.shu.edu.cn/mycourse/studentcourse?courseId=204664376&clazzid=10593708&enc=8782736c942a7296a38d6ca117ebfe5f')

for i in range(4,6) :
    coureses = driver.find_elements_by_class_name('articlename')
    gotocourse = webdriver.ActionChains(driver)
    gotocourse.click(coureses[i])
    gotocourse.perform()
    try :
        print('进入页面{}'.format(i))
        time.sleep(2)
        videotag = driver.find_element_by_id('dct1')
    except :
        print('未发现视频，返回')
        driver.back()
        continue
    title = driver.find_element_by_tag_name('h1').get_attribute('textContent')
    print(title)
    '''
    time.sleep(5)
    driver.switch_to.frame('iframe')
    video = driver.find_element_by_class_name('ans-attach-ct')
    playvideo = webdriver.ActionChains(driver)
    playvideo.click(video)
    playvideo.perform()
    print('开始播放')
    driver.switch_to.frame(0)
    time.sleep(3)
    while True :
        duration = driver.find_element_by_class_name('vjs-duration-display').get_attribute('textContent')
        now = driver.find_element_by_class_name('vjs-current-time-display').get_attribute('textContent')
        time.sleep(10)
        print('已播放{}/{}'.format(now,duration))
        if now == duration :
            break
        try :
            pass
        except: 
            continue
    '''
    driver.switch_to.default_content()
    testtag = driver.find_element_by_id('dct2')
    gotest = webdriver.ActionChains(driver)
    gotest.click(testtag)
    gotest.perform()



    time.sleep(3)
    driver.switch_to.frame('iframe')
    driver.switch_to.frame(0)
    driver.switch_to.frame('frame_content') 
    problems = driver.find_elements_by_css_selector('.Zy_TItle')


    anslist = []

    for j in problems:
        text = j.get_attribute('textContent')
        protext = findpro.findall(text)
        for k in protext:
            k = k.lstrip('】').rstrip('（')
            for l in range(len(lines)):
                words = str(lines[l].decode('utf-8'))
                if k in words:
                    break
            while True :
                words = str(lines[l].decode('utf-8'))
                if daan in words :
                    for m in words :
                        if m in answers:
                            anslist.append(m)
                            break
                    break
                else:
                    l += 1
        
    allinput = driver.find_elements_by_tag_name('input')
    allChoiceA = []
    allChoiceB = []
    allChoiceC = []
    allChoiceD = []
    allChoiceT = []
    allChoiceF = []
    for k in allinput :
        choiceValue = k.get_attribute('value')
        if choiceValue == 'A':
            allChoiceA.append(k)
        elif choiceValue == 'B':
            allChoiceB.append(k)
        elif choiceValue == 'C' :
            allChoiceC.append(k) 
        elif choiceValue == 'D':
            allChoiceD.append(k)
        elif choiceValue == 'true':
            allChoiceT.append(k)
        elif choiceValue == 'false':
            allChoiceF.append(k)

    countChoice = len(allChoiceA)

    for j in range(len(anslist)) :
        tempans = anslist[j]
        choose = webdriver.ActionChains(driver)
        if tempans == 'A' :
            target = allChoiceA[j]
        elif tempans == 'B':
            target = allChoiceB[j]
        elif tempans == 'C' :
            target = allChoiceC[j]
        elif tempans == 'D':
            target = allChoiceD[j]
        elif tempans == '√' :
            target = allChoiceT[j-countChoice]
        elif tempans == '×':
            target = allChoiceF[j-countChoice]
        driver.execute_script("arguments[0].scrollIntoView();",target)
        target.click()
        time.sleep(2)
    

    submitans = driver.find_element_by_css_selector('.Btn_blue_1')
    submitans.click()
    try :
        confirm = driver.find_element_by_class_name('bluebtn ')
        confirm.click()
    except :
        moveup = webdriver.ActionChains(driver)
        moveup.send_keys(Keys.PAGE_UP)
        moveup.perform()
        confirm = driver.find_element_by_class_name('bluebtn ')
        confirm.click()
    driver.back()
        