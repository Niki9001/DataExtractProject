
from selenium import webdriver
from bs4 import BeautifulSoup
import time  # 导入time模块
import random
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains



driver = webdriver.Firefox()

url='https://www.workopolis.com/jobsearch/find-jobs?ak=data%20scientist&l=Nova%20Scotia&job=A2ZjrNha9ejp6YmnLVpeLtCIK8aQsPP5ST5uuYRGl0XXtDgS49wKPq2kSYmtcSkP'
driver.get(url)

#生成0-1之间的随机数字
waitTime = random.random()
print(waitTime)

#用随机数字控制等待时间
time.sleep(waitTime*12)

#需要点击的网址位置
kw = driver.find_element(By.CSS_SELECTOR,'#job-list > article > h2 > a')
ActionChains(driver).context_click(kw).perform()
time.sleep(waitTime*1.1)
pyautogui.typewrite(['t'])

driver.switch_to.window(driver.window_handles[-1])

time.sleep(waitTime*10.978)
#接收js内容
# 获取新页面的HTML内容
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

title = soup.select('#main-content > div > aside ')
"""
companyName = soup.select('#main-content > div > aside > header > div > div.ViewJobHeaderMain > div.ViewJobHeaderCompany ')
location = soup.select('#main-content > div > aside > div > div > div > div.viewjob-entities ')
jobTab = soup.select('#main-content > div > aside > div > div > div > div.viewjob-entities')
requires = soup.select('#main-content > div > aside > div > div > div > div.viewjob-description.ViewJobBodyDescription > div')
"""
for each_title in title:
    print(each_title.text)
"""
for each_companyName in companyName:
    print(each_companyName.text)

for each_location in location:
    print(each_location.text)

for each_jobTab in jobTab:
    print(each_jobTab.text)

for each_requires in requires:
    print(each_requires.text)
    """
