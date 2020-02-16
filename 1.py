from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
daan = '答案'
file = open('answer.txt','rb')
answers = ['A','B','C','D','√','×']
lines = file.readlines()
findpro = re.compile(r'】.*?（')

SupportSchool = {'1':['上海大学','SHU']}
def login(school,username,password,WebDriver) :
    ''' 
    登录，参数:学校，用户名，密码，webdriver
    '''
    if school == 'SHU' :  # 上海大学
        WebDriver.get("http://www.elearning.shu.edu.cn/portal")
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
        # 跳转课程页面
        WebDriver.get('http://mooc1.elearning.shu.edu.cn/mycourse/studentcourse?courseId=204664376&clazzid=10593708&enc=8782736c942a7296a38d6ca117ebfe5f')
        return True
def FindCourse(WebDriver) :
    '''
    定位所有课
    '''
    courses = WebDriver.find_elements_by_class_name('articlename')
    return courses
def gotocourse(course,WebDriver) :
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
def FindVideoTag(WebDriver):
    '''
    定位视频标签，未找到则返回
    '''
    try :
        videotag = WebDriver.find_element_by_id('dct1')
        print('发现视频')
        return True
    except :
        print('未发现视频，返回')
        WebDriver.back()
        return False
def PlayVideo(WebDriver) :
    '''
    定位视频并播放
    '''
    video = WebDriver.find_element_by_class_name('ans-attach-ct')
    video.click()
    print('开始播放')
def isover(WebDriver) :
    '''
    视频是否结束
    '''
    duration = WebDriver.find_element_by_class_name('vjs-duration-display').get_attribute('textContent')
    now = WebDriver.find_element_by_class_name('vjs-current-time-display').get_attribute('textContent')    
    print('已播放{}/{}'.format(now,duration))
    return duration == now

# 启动浏览器
driver = webdriver.Chrome()  
# 登录并跳转到课程
Username = input('请输入用户名')
Password = input('请输入密码')
for i in SupportSchool :
    print(i,i[1][0],i[1][1])
SchoolName = SupportSchool[input()][1]


DoLogin = login(SchoolName,Username,Password,driver)
# 定位所有课
courses = FindCourse(driver)
for i in range(31,40) :
    # 定位所有课
    courses = FindCourse(driver)
    # 跳转到具体页面
    DoGotoCourse = gotocourse(courses[i],driver)
    # 显示标题
    time.sleep(2)
    ShowTitle(driver)
    # 寻找是否有视频，无则返回
    if not FindVideoTag(driver):
        continue
    driver.switch_to.frame('iframe')
    # 播放视频
    PlayVideo(driver)   
    driver.switch_to.frame(0)
    time.sleep(3)


    while not isover(driver) :       
        time.sleep(10)        
        try :
            ProblemChoices = driver.find_elements_by_name('ans-videoquiz-opt')
            SubmitAnswer = driver.find_element_by_class_name('ans-videoquiz-submit')
            for i in range(len(ProblemChoices)) :
                print(i)
                ProblemChoices = driver.find_elements_by_name('ans-videoquiz-opt')
                ProblemChoices[i].click()
              
                time.sleep(2)
                SubmitAnswer.click()
 
                time.sleep(2)
                alert = driver.switch_to.alert
                print(alert.text)
                alert.accept()
                
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
    problems = driver.find_elements_by_css_selector('.Zy_TItle')


    anslist = []

    for j in problems:
        text = j.get_attribute('textContent')
        protext = findpro.findall(text)
        for k in protext:
            k = k.lstrip('】').rstrip('（').rstrip('？').rstrip('。')
            for l in range(len(lines)):
                words = str(lines[l].decode('utf-8'))
                if k[2:-2] in words:
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
        print('第{}题，选择{}'.format(j,tempans))
        time.sleep(2)
    

    submitans = driver.find_element_by_css_selector('.Btn_blue_1')
    submitans.click()
   
    moveup = webdriver.ActionChains(driver)
    moveup.send_keys(Keys.PAGE_UP)
    moveup.perform()
    time.sleep(2)
    confirm = driver.find_element_by_class_name('bluebtn ')
    confirm.click()

    driver.get('http://mooc1.elearning.shu.edu.cn/mycourse/studentcourse?courseId=204664376&clazzid=10593708&enc=8782736c942a7296a38d6ca117ebfe5f')
        
        


    
    



    
        
   
    
    
