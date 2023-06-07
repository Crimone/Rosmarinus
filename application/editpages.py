from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

import os

#加载profile文件可以保持登录状态
profileDir = r'C:\Users\Crimone\AppData\Roaming\Mozilla\Firefox\Profiles\4ahrhkk0.default-release-1658510679158'
profile = webdriver.FirefoxProfile(profileDir)
driver = webdriver.Firefox(profile)

file = r'C:\Users\Crimone\source\repos\Rosmarinus\images'


#打开登录页面，url为要打开的地址
driver.get("http://backrooms-wiki-cn.wikidot.com/theme:aero-glass")

#最大化浏览器
driver.maximize_window()

#等待
time.sleep(2)

#元素定位登录按钮
edit = driver.find_element_by_id("more-options-button")
#点击登录
edit.click()

#元素定位登录按钮
edit = driver.find_element_by_id("backlinks-button")
#点击登录
edit.click()

time.sleep(2)

continue_link = driver.find_elements_by_link_text('Edit')

linklist = []

skip = True

for link in continue_link:

    if skip:
        ls = link.get_attribute('href')
        if ls.startswith('http://backrooms-wiki-cn.wikidot.com/between-the-pictures'):
            skip=False
    else:
        ls = link.get_attribute('href')
        if ls.startswith('http://backrooms-wiki-cn.wikidot.com/'):

            linklist.append(ls)

for s in linklist:
    driver.get(s)

    time.sleep(2)

    driver.execute_script(
        "WIKIDOT.modules.PageEditModule.listeners.forcePageEditLockRemove(event);"
    )

    time.sleep(2)

    um=driver.find_element_by_id('edit-page-textarea')#定位用户名输入框

    text_um="123"

    text_um=um.get_attribute('value')#获取文本框内已有的值

    text_um=text_um.replace("[[include :scp-wiki-cn:theme:basalt darkmode=a]]\n","")
    text_um=text_um.replace("https://crimone.github.io/rosmarinus/images/","https://evernight-aquarium.wdfiles.com/local--files/files/")
    text_um=text_um.replace("https://tvax4.sinaimg.cn/large/","https://evernight-aquarium.wdfiles.com/local--files/files/")
    text_um=text_um.replace("https://tva1.sinaimg.cn/large/","https://evernight-aquarium.wdfiles.com/local--files/files/")

    um.clear()

    um.send_keys(text_um)

    time.sleep(5)

    driver.execute_script(
        "WIKIDOT.modules.PageEditModule.listeners.save(event);"
    )  # js_code 换成你需要的js指令

    time.sleep(5)

