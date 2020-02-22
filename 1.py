# 导入
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re



# 定义常量
# 用于匹配题目的正则表达式
FindProblemText = re.compile(r'】.*?[？?（(。:]+')
# 用于匹配答案的字符串和列表
daan = '答案'
answers = ['A','B','C','D','√','×']
# 读取题库
file = open('answer.txt','rb')
lines = file.readlines()
file.close()
# 支持的学校
SupportSchool = {'1':['上海大学','SHU']}
for i in range(SupportSchool) :
    print(i,SupportSchool[i][0],SupportSchool[i][1])
# 学校，用户名，密码，课程链接
SchoolName = input('请输入学校序号')
UserName = input('请输入用户名')
Password = input('请输入密码')
ClassUrl = input('请输入课程链接')


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
        # 定位登录按钮并点击
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
def GotoClass(WebDriver) :
    '''
    前往课程页面，driver为必选参数，url默认参数为安全课程
    '''
    WebDriver.get(ClassUrl)
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
def ProbleminVideo(WebDriver) :
    '''
    处理视频中的题
    '''
    ProblemChoices = WebDriver.find_elements_by_name('ans-videoquiz-opt')
    SubmitAnswer = WebDriver.find_element_by_class_name('ans-videoquiz-submit')
    print('发现视频中题')
    for i in range(len(ProblemChoices)) :
        print('正在尝试第{}个选项'.format(i+1))
        ProblemChoices = WebDriver.find_elements_by_name('ans-videoquiz-opt')
        ProblemChoices[i].click()            
        time.sleep(2)
        SubmitAnswer.click()
        time.sleep(2)
        alert = driver.switch_to.alert
        alert.accept()
def FindProblems(WebDriver) :
    '''
    匹配所有题目的题干，返回一个题目列表
    '''
    text = WebDriver.find_elements_by_css_selector('.Zy_TItle')
    problems = []
    for i in range(len(text)) :
        ProblemText = text[i].get_attribute('textContent')
        ProblemText = FindProblemText.findall(ProblemText)[0]
        ProblemText = ProblemText.lstrip('】').rstrip('（').rstrip('？').rstrip('。').rstrip('(')
        problems.append(ProblemText)
    return problems
def FindAnswer(problem) :
    '''
    在题库中寻找题目的答案并返回
    '''
    j = 0
    for i in range(6805):
        words = str(lines[i].decode('utf-8'))
        if problem[2:-2]in words:
            j = i
            break
    while True :
        words = str(lines[j].decode('utf-8'))
        if daan in words :
            for char in words :
                if char in answers:
                    return char
            break
        else:
            j += 1
def FindProblemChoices(WebDriver) :
    '''
    寻找所有选项，返回一个字典
    '''
    AllChoices = {'A':[],'B':[],'C':[],'D':[],'':[],'×':[]}
    AllInput = WebDriver.find_elements_by_tag_name('input')
    for AInput in AllInput :
        ChoiceValue = AInput.get_attribute('value')
        if ChoiceValue =='true':
            ChoiceValue = '√'
        elif ChoiceValue == 'false':
            ChoiceValue = '×'
        try :
            AllChoices[ChoiceValue].append(AInput)
        except :
            pass
    return AllChoices
def AnswerProblem(num,answer,choices,WebDriver) :
    '''
    回答问题，三个参数：题号，答案，存储所有选项的字典
    '''
    target = choices[answer][num]
    WebDriver.execute_script("arguments[0].scrollIntoView();",target)
    target.click()
    print('第{}题，选择{}'.format(num+1,answer))
def SubmitAnswer(WebDriver) :
    '''
    提交答案
    '''
    SubmitButton = WebDriver.find_element_by_css_selector('.Btn_blue_1')
    SubmitButton.click()
    moveup = webdriver.ActionChains(WebDriver)
    moveup.send_keys(Keys.PAGE_UP)
    moveup.perform()
    time.sleep(2)
    confirm = WebDriver.find_element_by_class_name('bluebtn ')
    confirm.click()






# 启动浏览器
driver = webdriver.Chrome()  
# 登录并跳转到课程
login(SupportSchool[SchoolName][1],UserName,Password,driver)
# 前往指定课程
GotoClass(driver)
# 定位所有课
courses = FindCourse(driver)
for i in range(7,len(courses)) :
    # 定位所有课
    courses = FindCourse(driver)
    # 跳转到具体页面
    GotoCourse(courses[i],driver)
    # 显示标题
    time.sleep(2)
    ShowTitle(driver)
    driver.switch_to.frame(0)
    # 播放视频，无视频则返回
    videoes = FindViedo(driver)
    if len(videoes) == 0:
        print('无视频，返回')
        GotoClass(driver)
        continue
    for j in range(len(videoes)):
        videoes = FindViedo(driver)
        driver.execute_script("arguments[0].scrollIntoView();",videoes[j])
        videoes[j].click()
        print('开始播放视频')
        driver.switch_to.frame(videoes[j])
        time.sleep(15)
        # 视频是否结束
        while not isVideoOver(driver) :       
            time.sleep(10)      
            # 视频中是否有题，有则暴力尝试答题
            try :
                ProbleminVideo(driver)
            except: 
                continue  
        driver.switch_to.parent_frame()  
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
    # 寻找所有题目
    ProblemList = FindProblems(driver)
    # 匹配题目答案
    AnswerList = [FindAnswer(j) for j in ProblemList]
    print('题目答案：',AnswerList)    
    # 寻找所有选项，并给出选择题个数
    AllChoicesDict = FindProblemChoices(driver)
    CountChoice = len(AllChoicesDict['A'])
    # 回答问题
    for j in range(len(AnswerList)) :
        if AnswerList[j] == '×' or AnswerList[j] == '√':
            AnswerProblem(j-CountChoice,AnswerList[j],AllChoicesDict,driver)
        else :
            AnswerProblem(j,AnswerList[j],AllChoicesDict,driver)
        time.sleep(2)
    # 提交答案
    SubmitAnswer(driver)
    GotoClass(driver)



    '''
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
      