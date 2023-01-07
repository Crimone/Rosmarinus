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
        driver.get("http://scp-wiki-cn.wikidot.com/wanderers:conic-section-damn")

        #最大化浏览器
        driver.maximize_window()

        #等待
        time.sleep(2)
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        time.sleep(0.005)
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        time.sleep(0.005)
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        time.sleep(0.005)
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        time.sleep(0.1)
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )
        driver.execute_script(
            "WIKIDOT.modules.PageRateWidgetModule.listeners.rate(event, 1)"
        )

        time.sleep(2)

    except:
        pass