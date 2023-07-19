# Made By Mercuria

from selenium import webdriver
from datetime import datetime
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import re
import json


def short_sleep(min_time=2, max_time=5):
    time.sleep(random.uniform(min_time, max_time))

def long_sleep(min_time=10, max_time=15):
    time.sleep(random.uniform(min_time, max_time))

def find_ele_ment_with_retry(driver, by, locator, max_wait=10, retry_interval=2):
    wait = WebDriverWait(driver, max_wait)
    retry_count=0
    while retry_count < max_wait:
        try:
            element = wait.until(EC.presence_of_element_located((by, locator)))
            return element
        except:
            time.sleep(retry_interval)
            retry_count = retry_count + 1


def find_elements_with_retry(driver, by, locator, max_wait=10, retry_interval=2):
    wait = WebDriverWait(driver, max_wait)
    retry_count=0
    while retry_count < max_wait:
        try:
            elements = wait.until(EC.presence_of_all_elements_located((by, locator)))
            return elements
        except:
            time.sleep(retry_interval)
            retry_count = retry_count + 1
    return []



def main():

    options = webdriver.EdgeOptions()
    options.add_argument("-inprivate")

    driver = webdriver.Edge(options=options)

    data = []
    count = 0

    search_string="SNIS"

    while(1):

        count=count+1

        #打开登录页面，url为要打开的地址
        driver.get(f"https://missav.com/cn/chinese-subtitle?page={count}")

        #元素定位登录按钮
        datalist = find_elements_with_retry(driver,By.CSS_SELECTOR,'.thumbnail.group')

        if datalist==[]:
            break

        #保存为json文件
        
        for element in datalist:

            # 找到<div class="col-xs-12 col-sm-8 col-lg-9 file">元素
            div_element = element.find_element(By.CSS_SELECTOR,'a.text-secondary.group-hover\:text-primary')

            # 获取<div>元素的文本
            div_text = div_element.get_attribute('innerHTML')


            data.append({
                'title': div_text,
                'href': div_element.get_attribute('href')
            })

        with open(f'application/missav_list.json', 'w',encoding="utf-8-sig") as json_file:
            json.dump(data, json_file,ensure_ascii=False,indent=4)


        
        
            
        #点击登录
    

    

    
if __name__ == '__main__':
    main()
