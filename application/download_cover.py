from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

from tqdm import tqdm
import requests
import os
import argparse
import time

def main():
    parser = argparse.ArgumentParser(description='Fetch scans from bilibili') 
    parser.add_argument('path', help='The path to the directory')
    parser.add_argument('album', help='Album name')
    
    args = parser.parse_args()

    folder = args.path
    if os.path.isfile(folder):
        folder = os.path.dirname(folder)
    
    album = args.album

    print(album)

    options = Options()
    driver = webdriver.Edge()

    driver.get(f"https://space.bilibili.com/34075236/search/dynamic?keyword={album}")

    url = ""
    time.sleep(2.5)
    for a in driver.find_elements(By.TAG_NAME, "a"):
        if len(a.find_elements(By.CSS_SELECTOR, "span.dynamic-keyword")) > 0:
            url = a.get_attribute("href")
            break
            
    while url == "":
        if driver.current_url.startswith("https://www.bilibili.com/read/cv"):
            url = driver.current_url
        else:
            time.sleep(2.5)
    
    folder = os.path.join(folder, r"Scans")
    if not os.path.exists(folder):
        os.makedirs(folder)

    driver.get(url)

    images = driver.find_elements(By.CSS_SELECTOR, "#article-content img")
    count = 1
    for image in tqdm(images):
        img_url = image.get_attribute("data-src")
        if "@" in img_url:
            img_url = img_url.split("@")[0]
        img_name = "{:02d}.".format(count) + img_url.split(".")[-1]

        img_response = requests.get("https:" + img_url)

        with open(os.path.join(folder, img_name), "wb") as f:
            f.write(img_response.content)

        count += 1

    print("所有图片已下载到目录:", folder)

if __name__ == '__main__':
    main()