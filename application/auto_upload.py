from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from imgbbpy.imgbb import SyncClient
from tqdm import tqdm

import requests
import os
import subprocess
import argparse
import time
import re

import shutil

def copy_files_to_directory(src_dir, dest_dir):
    """
    复制src_dir目录中的所有文件到dest_dir目录
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dest_path)

def create_password_protected_rar(directory_to_rar, password):
    rar_path = "rar"  # 或使用确切的路径，例如rar_path = "C:\\Program Files\\WinRAR\\rar.exe"

    cmd = rf'.\rar a "-hp{password}" -rr5 -s "{directory_to_rar}.rar" "{directory_to_rar}"'
    result = subprocess.run(cmd, shell=True, check=True, cwd=r"D:\WinRAR")

def get_flac_titles(directory):
    titles = []

    # 遍历指定目录下的所有文件和子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 如果文件的扩展名是.flac
            if file.endswith('.flac'):
                title = os.path.splitext(file)[0]  # 去掉文件的扩展名
                titles.append(title)

    # 将标题列表连接成一个字符串，每个标题之间使用换行符分隔
    return '\n'.join(titles)

def find_element_with_retry(driver, by, locator, max_wait=10, retry_interval=2):
    wait = WebDriverWait(driver, max_wait)
    retry_count=0
    while retry_count < max_wait:
        try:
            element = wait.until(EC.presence_of_element_located((by, locator)))
            return element
        except:
            time.sleep(retry_interval)
            retry_count = retry_count + 1



def main():
    parser = argparse.ArgumentParser(description='Fetch scans from bilibili') 
    parser.add_argument('path', help='The path to the directory')
    parser.add_argument('album', help='Album name')
    
    args = parser.parse_args()

    folder = args.path
    if os.path.isfile(folder):
        folder = os.path.dirname(folder)
    
    album = args.album

    tempfolder = os.path.join("D:\\", os.path.basename(os.path.normpath(folder)))

    if not os.path.exists(tempfolder):
        copy_files_to_directory(folder, tempfolder)
    else:
        print(f"Folder {tempfolder} already exists. Skipping copy.")

    client = SyncClient('70943e307320801856c68c091b67f025')
    image = client.upload(file=os.path.join(tempfolder,"cover.jpg"))

    imgbb_url = image.url

    titles = get_flac_titles(tempfolder)

    copy_files_to_directory(r"F:\Downloads\压缩包必含文件", tempfolder)

    rar_password = 'www.cdbao.net'

    if not os.path.exists(tempfolder + ".rar"):
        create_password_protected_rar(tempfolder, rar_password)
    else:
        print(f"RAR file {tempfolder}.rar already exists. Skipping creation.")

    
    cmd = rf'.\BaiduPCS-Go.exe upload "{tempfolder}.rar" /cdbao'
    result = subprocess.run(cmd, shell=True, check=True, cwd=r"C:\Users\Crimone\Downloads\BaiduPCS-Go-v3.9.5-windows-x64")

    cmd = rf'.\BaiduPCS-Go.exe share set "/cdbao/{tempfolder}.rar"'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=r"C:\Users\Crimone\Downloads\BaiduPCS-Go-v3.9.5-windows-x64")

    # Wait for the process to complete and get the output and error streams
    stdout, stderr = process.communicate()

    # Convert the byte stream to string
    stdout_str = stdout.decode('utf-8')

    link = ""
    password = ""

    link_match = re.search(r'链接: (https://[^,]+)', stdout_str)
    password_match = re.search(r'密码: (\w+)', stdout_str)

    if link_match and password_match:
        link = link_match.group(1)
        password = password_match.group(1)
        print(f"链接: {link}")
        print(f"密码: {password}")
    else:
        print("未找到链接或密码")

    profileDir = r'C:\Users\Crimone\AppData\Roaming\Mozilla\Firefox\Profiles\ikgg20dk.default-release'
    profile = webdriver.FirefoxProfile(profileDir)
    driver = webdriver.Firefox(profile)

    driver.get(f"https://www.cdbao.net/forum.php?mod=post&action=newthread&fid=178")

    time.sleep(5)

    username = find_element_with_retry(driver,By.CSS_SELECTOR,'input[name="username"]')
    username.send_keys("mercuresphere")

    pwd = find_element_with_retry(driver,By.CSS_SELECTOR,'input[name="password"]')
    pwd.send_keys("Lxh112858_")

    loginbutton = find_element_with_retry(driver,By.CSS_SELECTOR,'button[name="loginsubmit"]')

    loginbutton.click()

    time.sleep(10)

    driver.refresh()

    # 定位<select>元素
    select_element = find_element_with_retry(driver,By.CSS_SELECTOR,"div#typeid_ctrl_menu.sltm ul li:last-child")

    # 创建一个Select对象
    driver.execute_script("arguments[0].click();", select_element)

    title = find_element_with_retry(driver,By.CSS_SELECTOR,"input#subject.px")

    title.send_keys(os.path.basename(folder))

    find_element_with_retry(driver,By.CSS_SELECTOR,"label#e_switcher.bar_swch.ptn").click()

    textarea = find_element_with_retry(driver,By.CSS_SELECTOR,"textarea#e_textarea.pt")

    driver.execute_script("arguments[0].value = arguments[1];", textarea, f"[img]{imgbb_url}[/img]\n\n{titles}\n\n[hide]链接：{link}, 密码：{password}[/hide]")

    submitbutton = find_element_with_retry(driver,By.CSS_SELECTOR,"button#postsubmit")

    submitbutton.click()

    time.sleep(2.5)


if __name__ == '__main__':
    main()