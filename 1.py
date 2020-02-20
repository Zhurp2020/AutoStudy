from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

findpro = re.compile(r'】.*?[？?（(。:]+')

SupportSchool = {'1':['上海大学','SHU']}
def login(school,username,password,WebDriver) :
    ''' 
    登录，参数:学校，用户名，密码，webdriver
    '''
    if school == 'SHU' :  # 上海大学
        while True :
            try :
                WebDriver.get("http://www.elearning.shu.edu.cn/portal")
                break
            except :
                continue
        # 登录按钮
        LoginButton = WebDriver.find_element_by_css_selector('.loginSub') 
        LoginButton.click()
        # 用户名密码输入框，提交按钮
        UsernameInput = WebDriver.find_element_by_name('username')
        PasswordInput = WebDriver.find_element_by_name('password')
        LoginSubmit = WebDriver.find_element_by_name('login_submit')
        # 输入用户名密码，提交       
        InputAction = webdriver.ActionChains(WebDriver)
        InputAction.click(UsernameInput)
        InputAction.send_keys_to_element(UsernameInput,username)
        InputAction.click(PasswordInput)
        InputAction.send_keys_to_element(PasswordInput,password)
        InputAction.click(LoginSubmit)
        InputAction.perform()
def GotoClass(WebDriver,url = 'http://mooc1.elearning.shu.edu.cn/mycourse/studentcourse?courseId=204664376&clazzid=10593708&enc=8782736c942a7296a38d6ca117ebfe5f') :
    '''
    前往课程页面，driver为必选参数，url默认参数为安全课程
    '''
    WebDriver.get(url)
def FindViedo (WebDriver) :
    '''
    寻找视频
    '''
    VideoList = []
    VideoClassName = 'ans-insertvideo-online'
    frames = WebDriver.find_elements_by_tag_name('iframe')
    for i in range(len(frames)):
        frames = WebDriver.find_elements_by_tag_name('iframe')
        classname = frames[i].get_attribute('class')
        if VideoClassName in classname :
            VideoList.append(frames[i])
    return VideoList
def FindCourse(WebDriver) :
    '''
    定位所有课
    '''
    courses = WebDriver.find_elements_by_class_name('articlename')
    return courses
def GotoCourse(course,WebDriver) :
    '''
    下拉到一节课，然后跳转，参数：课，driver
    '''
    WebDriver.execute_script("arguments[0].scrollIntoView();",course)
    course.click()
    return True
def ShowTitle(WebDriver) :
    '''
    显示小节标题
    '''
    title = WebDriver.find_element_by_tag_name('h1').get_attribute('textContent')
    print(title)
def FindTestTag(WebDriver):
    '''
    定位答题标签
    '''
    TestTag = WebDriver.find_element_by_id('dct2')
    print('发现题目')
    TestTag.click()
def PlayVideo(WebDriver) :
    '''
    定位视频并播放
    '''
    video = WebDriver.find_element_by_class_name('ans-attach-ct')
    video.click()
    print('开始播放')
def isVideoOver(WebDriver) :
    '''
    视频是否结束
    '''
    duration = WebDriver.find_element_by_class_name('vjs-duration-display').get_attribute('textContent')
    now = WebDriver.find_element_by_class_name('vjs-current-time-display').get_attribute('textContent')    
    print('已播放{}/{}'.format(now,duration))
    return duration == now
def findanswer(problem) :
    print(problem)
    n = 0
    daan = '答案'
    file = open('answer.txt','rb')
    answers = ['A','B','C','D','√','×']
    lines = file.readlines()
    file.close()
    for i in range(2638):
        words = str(lines[i].decode('utf-8'))
        if problem[2:-2]in words:
            n = i
            break
    while True :
        words = str(lines[n].decode('utf-8'))
        if daan in words :
            for j in words :
                if j in answers:
                    return j
            break
        else:
            n += 1

# 启动浏览器
driver = webdriver.Chrome()  
# 登录并跳转到课程
Username = input('请输入用户名')
Password = input('请输入密码')
for i in SupportSchool :
    print(i,i[1][0],i[1][1])
SchoolName = SupportSchool[input()][1]
login(SchoolName,Username,Password,driver)
# 前往指定课程
GotoClass(driver)
# 定位所有课
courses = FindCourse(driver)
count = 1
for i in range(130,160) :
    # 定位所有课
    courses = FindCourse(driver)
    # 跳转到具体页面
    DoGotoCourse = GotoCourse(courses[i],driver)
    # 显示标题
    time.sleep(2)
    ShowTitle(driver)
    # 寻找是否有视频，无则返回
    try:
        VideoTag = driver.find_element_by_id('dct1')
    except :
        print('未发现视频，返回')
        GotoClass(driver)
        continue
    driver.switch_to.frame(0)
    # 播放视频
    videoes = FindViedo(driver)
    for avideo in videoes:
        avideo.click()
        driver.switch_to.frame(avideo)
    time.sleep(10)
    
    while not isVideoOver(driver) :       
        time.sleep(10)        
        try :
            ProblemChoices = driver.find_elements_by_name('ans-videoquiz-opt')
            SubmitAnswer = driver.find_element_by_class_name('ans-videoquiz-submit')
            for i in range(len(ProblemChoices)) :
                ProblemChoices = driver.find_elements_by_name('ans-videoquiz-opt')
                ProblemChoices[i].click()            
                time.sleep(2)
                SubmitAnswer.click()
 
                time.sleep(2)
                alert = driver.switch_to.alert
                alert.accept()
        except: 
            continue
    
    driver.switch_to.default_content()
    # 检查是否有题，有则跳转，否则进入下一课
    try :
        FindTestTag(driver)
    except :
        GotoClass(driver)
        continue

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
            k = k.lstrip('】').rstrip('（').rstrip('？').rstrip('。').rstrip('(')
            m = findanswer(k)
            anslist.append(m)
            
    print(anslist)    
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
        print('第{}题，选择{}'.format(j+1,tempans))
        time.sleep(2)
    

    submitans = driver.find_element_by_css_selector('.Btn_blue_1')
    submitans.click()
    '''
    if count >= 2 :
        driver.switch_to.default_content()
        image = driver.find_element_by_id('imgVerCode')
        print('输入验证码')
        vercode = input()
        vercodeinput = driver.find_element_by_class_name('zc_input32')
        confirmbtn = driver.find_element_by_class_name('zc_btn')
        invercode = webdriver.ActionChains(driver)
        invercode.click(vercodeinput)
        invercode.send_keys_to_element(vercodeinput,vercode)
        invercode.click(confirmbtn)
        invercode.perform()
        driver.switch_to.frame('iframe')
        driver.switch_to.frame(0)
        driver.switch_to.frame('frame_content') 
    '''
    
    moveup = webdriver.ActionChains(driver)
    moveup.send_keys(Keys.PAGE_UP)
    moveup.perform()
    time.sleep(2)
    confirm = driver.find_element_by_class_name('bluebtn ')
    confirm.click()
    count += 1
    driver.get('http://mooc1.elearning.shu.edu.cn/mycourse/studentcourse?courseId=204664376&clazzid=10593708&enc=8782736c942a7296a38d6ca117ebfe5f')
        
        