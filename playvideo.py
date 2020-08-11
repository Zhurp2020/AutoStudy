from main import *


# 启动浏览器
driver = webdriver.Chrome()  
# 登录并跳转到课程
login(SchoolName,UserName,Password,driver)
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
    audio = FindAudio(driver)
    if len(videoes) == 0 and len(audio) == 0:
        print('无视频，返回')
        GotoClass(driver)
        continue
    for j in range(len(videoes)):
        print('2')
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
    for j in range(len(audio)):
        print('1')
        audio = FindAudio(driver)
        driver.execute_script("arguments[0].scrollIntoView();",audio[j])
        driver.switch_to.frame(audio[j])
        PlayAudio(driver)
        print('开始播放音频')
        time.sleep(15)
        # 视频是否结束
        while not isVideoOver(driver) :       
            time.sleep(10)      
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
    