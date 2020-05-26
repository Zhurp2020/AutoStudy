from main import *
import time

driver = webdriver.Chrome()  
# 登录并跳转到课程
login(SchoolName,UserName,Password,driver)
# 前往指定课程
GotoClass(driver)
while True :
    MissionUrl = input('输入任务点链接')
    driver.get(MissionUrl)
    driver.switch_to.frame(0)
    FileIds = FindFile(driver)
    print(FileIds)
    for i in FileIds:
        time.sleep(5)
        driver.get('http://d0.ananas.chaoxing.com/download/'+i)

