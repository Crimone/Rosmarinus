from selenium import webdriver
import time

#加载profile文件可以保持登录状态
profileDir = r'C:\Users\Crimone\AppData\Roaming\Mozilla\Firefox\Profiles\4ahrhkk0.default-release-1658510679158'
profile = webdriver.FirefoxProfile(profileDir)
driver = webdriver.Firefox(profile)

count = 2157
content = 1111

while 1:
    try:
        #打开登录页面，url为要打开的地址
        driver.get("http://evernight-aquarium.wikidot.com/admin:test2")

        #最大化浏览器
        driver.maximize_window()

        #等待
        time.sleep(2)

        #元素定位登录按钮
        edit = driver.find_element_by_id("edit-button")
        #点击登录
        edit.click()

        #等待
        time.sleep(5)

        driver.execute_script(
            "WIKIDOT.modules.PageEditModule.listeners.forcePageEditLockRemove(event);"
        )

        #等待
        time.sleep(5)

        #元素定位用户名输入框
        textbox = driver.find_element_by_id("edit-page-textarea")
        #输入用户名
        textbox.clear()
        output = "test" + str(content)
        textbox.send_keys(output)
        content=content+1

        #等待
        time.sleep(5)

        driver.execute_script(
            "WIKIDOT.modules.PageEditModule.listeners.save(event);"
        )  # js_code 换成你需要的js指令

        time.sleep(5)

        #发帖
        
        driver.get(
            "http://evernight-aquarium.wikidot.com/forum/t-15503295/test2")

        driver.execute_script(
            "WIKIDOT.modules.ForumViewThreadModule.listeners.newPost(event,null);"
        )

        time.sleep(5)

        textbox = driver.find_element_by_id("np-title")
        #输入用户名
        output = "test" + str(count)
        textbox.send_keys(output)

        count = count + 1

        textbox = driver.find_element_by_id("np-text")
        #输入用户名
        output = "test" + str(count)
        textbox.send_keys(output)

        count = count + 1

        driver.execute_script(
            "WIKIDOT.modules.ForumNewPostFormModule.listeners.save(event);")

        time.sleep(5)

    except:
        pass