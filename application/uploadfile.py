from selenium import webdriver
import time

import os

#加载profile文件可以保持登录状态
profileDir = r'C:\Users\Crimone\AppData\Roaming\Mozilla\Firefox\Profiles\4ahrhkk0.default-release-1658510679158'
profile = webdriver.FirefoxProfile(profileDir)
driver = webdriver.Firefox(profile)

file = r'C:\Users\Crimone\source\repos\Rosmarinus\transfer'

for root, dirs, files in os.walk(file):
    for file in files:
        path = os.path.join(root, file)
        print(path)

        try:

            time.sleep(8)

            #打开登录页面，url为要打开的地址
            driver.get("http://evernight-aquarium.wikidot.com/files/noredirect/true")

            #最大化浏览器
            driver.maximize_window()

            #等待
            time.sleep(2)

            #元素定位登录按钮
            edit = driver.find_element_by_id("files-button")
            #点击登录
            edit.click()

            time.sleep(2)

            edit = driver.find_element_by_id("show-upload-button")
            edit.click()

            time.sleep(2)

            filebox = driver.find_element_by_id("upload-userfile")

            filebox.send_keys(path)

            time.sleep(2)

            driver.execute_script("WIKIDOT.modules.PageUploadModule.listeners.checkFileExists(event)")
        
        except:
            pass    
