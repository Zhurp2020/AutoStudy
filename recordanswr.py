import main
from main import *


# 启动浏览器
driver = webdriver.Chrome()  
# 登录并跳转到课程
login(SchoolName,UserName,Password,driver)
# 前往指定课程
GotoClass(driver)
# 定位所有课
courses = FindCourse(driver)
for i in range(65,len(courses)) :
    # 定位所有课
    courses = FindCourse(driver)
    # 跳转到具体页面
    GotoCourse(courses[i],driver)
    # 显示标题
    time.sleep(2)
    ShowTitle(driver)
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
    problems = FindProblems(driver)
    MyAnswers = driver.find_elements_by_class_name('Py_answer')
    AnswerList = []
    for elem in MyAnswers :
        MyAnswer = elem.find_element_by_tag_name('span').get_attribute('textContent')
        AnswerList.append(MyAnswer)
    with open('securityanswer.txt','a',encoding= 'utf-8') as file :
        for j in range(len(problems)) :
            file.writelines([problems[j],'\n',AnswerList[j],'\n'])
    time.sleep(30)
    GotoClass(driver)
    print(i)