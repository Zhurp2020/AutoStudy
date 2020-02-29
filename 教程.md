---
title: 如何优雅地刷学习通课程
date: 2020-02-22 14:00:34
tags:
  - python
  - github
categories: Tech
summary: 基于python和Selenium的学习通刷课脚本
---
# 如何优雅地刷学习通课程
项目Github地址：[这里](https://github.com/Zhurp2020/AutoStudy)
克隆这个仓库：
``` bash
$ git clone https://github.com/Zhurp2020/AutoStudy.git
```
## 工具安装
+ python
+ 一个编辑器，推荐使用VS Code
+ （非常推荐）分布式版本控制工具Git
+ Selenium库
+ Chorme Webdriver
1. python   
   &emsp;&emsp;在官网[这里](https://www.python.org/)下载Python并安装
   ![python官网](/pics/pic2/1.jpg)
2. VS Code  
   &emsp;&emsp;访问[这里](https://code.visualstudio.com/)下载安装VS Code。然后在扩展商店里安装python扩展。  
   ![VS Code官网](/pics/pic0/0.jpg) 
   ![python扩展](/pics/pic2/2.jpg) 
3. Git   
   &emsp;&emsp;访问[这里](https://git-scm.com/)下载安装git，然后完成相关配置。  
![git官网](/pics/Pic0/1.jpg)
4. Selenium库  
   &emsp;&emsp;可以使用`pip`安装这个库
   ``` bash
   pip install selenium
   ```
   &emsp;&emsp;这是一个自动化测试库，他可以自动操作浏览器。比如：访问页面，定位元素，输入点击等等。
5. Chorme Webdriver  
   &emsp;&emsp;访问[这里](https://chromedriver.chromium.org/downloads)下载chorme Webdriver，注意**一定要和当前使用的chorme版本相对应！**
   ![chorme Webdriver](/pics/pic2/3.jpg)
   &emsp;&emsp;下载完成后，把他解压，然后把`chormedriver.exe`移到python的安装目录下，这个目录看起来可能是这样的：`C:\Users\Administrator\AppData\Local\Programs\Python\Python38`
## 代码
selenium的官方文档在[这里](https://www.selenium.dev/documentation/zh-cn/getting_started/)  
找一个文件夹，新建一个`.py`文件，然后开始撸代码吧！  
先导入模块  
```python
import selenium
```
### 第一步
&emsp;&emsp;首先启动一个浏览器。当然除了chorme，selenium库还支持firefox等其他主流浏览器。这里用chorme作为例子。新建一个webdriver对象：
```python
driver = webdriver.Chrome() 
```
&emsp;&emsp;通过`webdriver.get(url)`方法访问一个页面。注意这个方法不会新建一个标签页，而是直接在当前页面上跳转。
```python
driver.get('http://www.elearning.shu.edu.cn/portal')
```
&emsp;&emsp;可以运行测试一下效果
![](/pics/pic2/4.jpg)
### 定位并操作元素
&emsp;&emsp;接下来，我们要做的是点击登录按钮。首先，我们要在页面上定位这个按钮。selenium提供了数种方法定位元素。例如`webdriver.find_element_by_class_name(name)`将返回匹配`class`是`name`的元素。此外，还可以通过`tag_name`、`id`、`css_selector`、`link_text`、`name`、`partial_link_text`、`xpath`等匹配元素。`webdriver.find_element_by_class_name(name)`将返回第一个匹配的元素。相应地，`webdriver.find_elements_by_class_name(name)`则会返回一个由所有找到的元素组成的`list`  
&emsp;&emsp;按下`F12`或鼠标右键检查可以查看网页的源代码。点击代码中的元素，我们可以看见相应的蓝框。一步步缩小范围，最终可以找到相应的代码。
![登录按钮的代码](/pics/pic2/5.jpg)
```html
<input type="button" value="登录" class="loginSub" onclick="goPassport2Login();">
```
&emsp;&emsp;那么，就可以写出定位该元素的代码
```python
LoginButton = driver.find_element_by_class_name('loginSub') 
```
&emsp;&emsp;通过`webelement.click()`方法可以点击该元素。
```python
LoginButton.click()
```
&emsp;&emsp;接下来，就跳转到了登录页面。在这个页面，需要定位三个元素：用户名和密码的输入框以及登录按钮。
![登录页面](/pics/pic2/6.jpg)
```html
<input type="text" name="username" id="username" placeholder="请输入账号/Campus ID Number">
<input type="password" name="password" id="password" placeholder="请输入密码/Password">
<input type="submit" name="login_submit" id="login-submit" value="登录/Login">
```
### 登录
&emsp;&emsp;写出定位这三个元素的代码
```python
UsernameInput = WebDriver.find_element_by_name('username')
PasswordInput = WebDriver.find_element_by_name('password')
LoginSubmit = WebDriver.find_element_by_name('login_submit')
```
&emsp;&emsp;这里我们需要进行五个操作：分别点击两个输入框并输入用户名和密码，点击登录按钮。可以用到Action Chain（动作链）。先通过`webdriver.AnctionChains(driver)`方法创建一个动作链：
```python
InputAction = webdriver.ActionChains(driver)
```
&emsp;&emsp;然后是点击和输入的操作。`.send_keys_to_element(element,keys_to_send)`用来模拟键盘输入。

```python
username = '' #你的用户名
password = '' #你的密码

InputAction.click(UsernameInput)
InputAction.send_keys_to_element(UsernameInput,username)
InputAction.click(PasswordInput)
InputAction.send_keys_to_element(PasswordInput,password)
InputAction.click(LoginSubmit)
```
&emsp;&emsp;最后，执行这个动作链。
```python
InputAction.perform()
```
&emsp;&emsp;可以把登录封装成一个函数。
```python
def login(username,password,WebDriver) :
    ''' 
    登录，参数:学校，用户名，密码，webdriver
    '''
    WebDriver.get("http://www.elearning.shu.edu.cn/portal")
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
```
### 播放视频
&emsp;&emsp;仿照以上的函数，可以很容易地写出跳转的课程页面、找到所有任务点，跳转并显示标题的功能。
```python
Classurl = '' # 课程链接
def GotoClass(WebDriver) :
    '''
    前往课程页面，driver为必选参数
    '''
    WebDriver.get(ClassUrl)
def FindCourse(WebDriver) :
    '''
    定位所有课
    '''
    courses = WebDriver.find_elements_by_class_name('articlename')
    return courses
def ShowTitle(WebDriver) :
    '''
    显示小节标题
    '''
    title = WebDriver.find_element_by_tag_name('h1').get_attribute('textContent')
    print(title)
```
&emsp;&emsp;这些函数代码可以保存在`main.py`中，然后新建一个`playvideo.py`文件，调用这些函数。可以使用`time.sleep(2)`来加长等待，模仿人类操作。
```python
from main import *


# 启动浏览器
driver = webdriver.Chrome()  
# 登录并跳转到课程
login(SchoolName,UserName,Password,driver)
# 前往指定课程
GotoClass(driver)
# 定位所有课
courses = FindCourse(driver)
for i in range(len(courses)) :
    # 定位所有课
    courses = FindCourse(driver)
    # 跳转到具体页面
    GotoCourse(courses[i],driver)
    # 显示标题
    time.sleep(2)
    ShowTitle(driver)
```
&emsp;&emsp;于是我们可以来到视频页面，开始定位视频。要点击视频播放，只要点击相应的`<iframe>`元素即可。这里我们遇到了第一个问题，直接定位会报错，因为这个元素本身也在一个`<iframe>`里面。由于代码比较长，这里省略了一部分
```html
<iframe height="2017" id="iframe" f src="/knowledge/..." ...>
    # document
        ...
        <iframe ... class="ans-attach-online ans-insertvideo-online" ...></iframe>
        <iframe ... class="ans-attach-online ans-insertvideo-online" ...></iframe>
        <iframe ... class="ans-attach-online insertdoc-online-ppt" ..."></iframe>
      ...
</iframe>
```
&emsp;&emsp;要定位到`<iframe>`里面的元素，需要使用`webdriver.switch_to.frame(frame_reference)`方法。参数`frame_reference`可以是`name`，整数或者一个`webelement`。
```python
driver.switch_to.frame(0) # 切换到第一个iframe
# 也可以这样
driver.switch_to.frame('iframe')
```
&emsp;&emsp;接下来会遇到第二个问题，页面上不止一个`<iframe>`，有的是视频而有的不是，比如第一第二个是视频，而第三个是PPT。简单观察可以看出，关键是`class`属性中是否有`ans-insertvideo-online`。而通过`.get_attribute('')`方法可以获得一个属性。于是可以写一个函数，返回一个所有符合条件的`<iframe>`列表。
```python
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
```
&emsp;&emsp;然后点击每一个元素，而如果页面上没有视频，则返回上一个页面。当然，这里有一个问题，还需要滚动页面到这个元素。selenium没有滚动屏幕的方法，可以借助js实现。
```python
videoes = FindViedo(driver)
    if len(videoes) == 0:
        print('无视频，返回')
        GotoClass(driver)
        continue
    for j in range(len(videoes)):
        videoes = FindViedo(driver)
        driver.execute_script("arguments[0].scrollIntoView();",videoes[j]) # 滚动屏幕到这个元素
        videoes[j].click()
        print('开始播放视频')
```
### 视频中的问题
&emsp;&emsp;接下来判断视频是否结束。首先切换到这个`iframe`。
```python
driver.switch_to.frame(videoes[j])
time.sleep(15)
```
&emsp;&emsp;然后找到进度条下面的现在时间和视频时间的元素。
```html
<span class="vjs-current-time-display" aria-live="off">0:03</span>
<span class="vjs-duration-display" aria-live="off">13:18</span>
```
&emsp;&emsp;于是就可以获得相应的属性，判断视频是否结束。
```python
def isVideoOver(WebDriver) :
    '''
    视频是否结束
    '''
    duration = WebDriver.find_element_by_class_name('vjs-duration-display').get_attribute('textContent')
    now = WebDriver.find_element_by_class_name('vjs-current-time-display').get_attribute('textContent')    
    print('已播放{}/{}'.format(now,duration))
    return duration == now
```
&emsp;&emsp;然后是视频中的题。这些题是可以暴力尝试答案的，只需要定位相应的选项和提交就可以了。题是随机出现的，html代码这里就不放了。注意当回答错误时，会弹出一个警告框，需要点掉才能继续操作。可以用`driver.switch_to.alert`方法切换到这个警告框，用`.accept()`方法接受（相当于点击确定按钮）。
```python
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
        alert = WebDriver.switch_to.alert
        alert.accept()
```
&emsp;&emsp;使用`try...except...`来处理这些随机出现的题，然后每隔10秒检查是否结束。
```python
while not isVideoOver(driver) :       
    time.sleep(10)      
    # 视频中是否有题，有则暴力尝试答题
    try :
        ProbleminVideo(driver)
    except: 
        continue
```
&emsp;&emsp;视频结束后，需要返回上一级`iframe`。
```python
driver.switch_to.parent_frame() 
```
&emsp;&emsp;所有视频结束后，还要返回默认`iframe`。
```python
driver.switch_to.default_content()
```
### 答题
&emsp;&emsp;定位跳转到章节测验的按钮。
```html
<span title="章节测验" onclick="changeDisplayContent(2,2,'162839918','204664376','10593708','');" id="dct2" class="c2 ">章节测验</span>
```
```python
def FindTestTag(WebDriver):
    '''
    定位答题标签
    '''
    TestTag = WebDriver.find_element_by_id('dct2')
    print('发现题目')
    TestTag.click()
```
&emsp;&emsp;点击跳转
```python
# 检查是否有题，有则跳转，否则进入下一课
try :
    FindTestTag(driver)
except :
    GotoClass(driver)
    continue
```
&emsp;&emsp;题目藏得挺深，需要连续切换三层`iframe`。
```html
<iframe height="2955" id="iframe" frameborder="0" scrolling="no" ... >
    # document
    ...
    <iframe ... frameborder="0" scrolling="no" width="650" ...  style="height: 1382px;">
        ...
        # document
        <iframe id="frame_content" name="frame_content" ... ></iframe>
    ...
    </iframe>
    ...
</iframe>
```
```python
time.sleep(3)
driver.switch_to.frame('iframe')
driver.switch_to.frame(0)
driver.switch_to.frame('frame_content') 
```
&emsp;&emsp;定位所有选项和题目。
```html
<div style="width:80%;height:100%;float:left;">【单选题】人类在阶级社会当中解决安全问题最大的一种手段是（）。</div> 
<!--> 题目长这样
 题目我全做完了，很遗憾无法展示选项的代码 <-->
```
&emsp;&emsp;题目的定位比较麻烦，元素本身没有提供可以供定位的信息，可以使用css选择器定位。在界面右侧找到相应的css文件，点进去可以直接找到这一行。
```css
.Zy_TItle i{width:55px;font-size:24px;color:#000000;text-align:center;}
```
&emsp;&emsp;然后就可以获取它的属性，然后用正则表达式加字符串切片匹配题干。这里写的比较糙，最终也没能找到一个完美的匹配方案。但是已经可以解决大部分问题了。
```python
import re

# 用于匹配题目的正则表达式
FindProblemText = re.compile(r'】.*?[？?（(。:：]+')
FindChineseText = re.compile(r'[\u4e00-\u9fa5]+')

def FindProblems(WebDriver) :
    '''
    匹配所有题目的题干，返回一个题目列表
    '''
    text = WebDriver.find_elements_by_css_selector('.Zy_TItle')
    problems = []
    for i in range(len(text)) :
        ProblemText = text[i].get_attribute('textContent')
        try :
            ProblemText = FindProblemText.findall(ProblemText)[0]
        except :
            ProblemText = FindChineseText.findall(ProblemText)[0]
        ProblemText = ProblemText.lstrip('】').rstrip('（').rstrip('？').rstrip('。').rstrip('(')
        problems.append(ProblemText)
    return problems
```
&emsp;&emsp;然后是定位选项，这个比较好办。
```python
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
```
&emsp;&emsp;接着在题库中寻找答案
```python
# 用于匹配答案的字符串和列表
daan = '答案'
answers = ['A','B','C','D','√','×']
# 读取题库
file = open('answer.txt','rb')
lines = file.readlines()
file.close()

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
```
&emsp;&emsp;然后答题就可以了。注意要计算一下选择题的个数。
```python
def AnswerProblem(num,answer,choices,WebDriver) :
    '''
    回答问题，三个参数：题号，答案，存储所有选项的字典
    '''
    target = choices[answer][num]
    WebDriver.execute_script("arguments[0].scrollIntoView();",target)
    target.click()
    print('第{}题，选择{}'.format(num+1,answer))
```
```python
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
```
&emsp;&emsp;最后一步，提交答案。注意这里需要向上滚动一下，执行js不管用，可以用按一下page up键解决。
```python
from selenium.webdriver.common.keys import Keys

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
```
&emsp;&emsp;执行，然后返回课程页面，继续下一课，搞定~
```python
# 提交答案
SubmitAnswer(driver)
GotoClass(driver)
```