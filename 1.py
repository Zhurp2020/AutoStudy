from selenium import webdriver
import time
import re

daan = '答案'
file = open('answer.txt','rb')
answers = ['A','B','C','D','√','×']
lines = file.readlines()

username = input('用户名')
password = input('密码')

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
inputaction.send_keys_to_element(userin,'')
inputaction.click(pwdin)
inputaction.send_keys_to_element(pwdin,'')
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

    driver.switch_to.default_content()
    testtag = driver.find_element_by_id('dct2')
    gotest = webdriver.ActionChains(driver)
    gotest.click(testtag)
    gotest.perform()



    time.sleep(3)
    driver.switch_to.frame('iframe')
    driver.switch_to.frame(0)
    driver.switch_to.frame('frame_content') 
    porblems = driver.find_elements_by_css_selector('.Zy_TItle')


    anslist = []

    for j in porblems:
        text = j.get_attribute('textContent')
        protext = findpro.findall(text)
        for k in protext:
            k = k.lstrip('】').rstrip('（')
            print(k)
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
    allchoiceA = []
    for j in allinput :
        if j.get_attribute('value') == 'A':
            allchoiceA.append(j)
            tempA = j
            print('yes')
            break
    
    choose = webdriver.ActionChains(driver)
    choose.click(tempA)
    choose.perform()
    