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

import string
import imaplib
import email
from email.header import decode_header

# 你的Outlook邮箱的用户名和密码
username = "a826944805@outlook.com"
password = "H3llo2U1"

# 

def get_latest_mail():
    # 创建IMAP4类与服务器进行通信
    mail = imaplib.IMAP4_SSL("outlook.office365.com")

    # 通过用户名和密码进行认证
    mail.login(username, password)

    # 选择邮箱
    mail.select("inbox")

    # 搜索邮件
    result, data = mail.uid('search', None, '(HEADER Subject "Slack ")')

    # 获取所有邮件ID
    inbox_item_list = data[0].split()

    # 获取最新的邮件ID
    latest_email_id = inbox_item_list[-1]

    result2, email_data = mail.uid('fetch', latest_email_id, '(BODY[HEADER])')
    raw_email = email_data[0][1].decode("utf-8")
    email_message = email.message_from_string(raw_email)

    # 获取邮件主题
    subject = decode_header(email_message['Subject'])[0][0]
    if isinstance(subject, bytes):
        subject = subject.decode()
    return subject.rsplit("：", 1)[-1]

def short_sleep(min_time=2, max_time=5):
    time.sleep(random.uniform(min_time, max_time))

def long_sleep(min_time=10, max_time=15):
    time.sleep(random.uniform(min_time, max_time))

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

def click_element_with_retry(driver, by, locator, max_wait=10, retry_interval=2):
    wait = WebDriverWait(driver, max_wait)
    retry_count=0
    while retry_count < max_wait:
        try:
            element = wait.until(EC.presence_of_element_located((by, locator)))
            element.click()
            return
        except:
            time.sleep(retry_interval)
            retry_count = retry_count + 1

def create_new_area(driver):
    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="landing_view_confirm_button"]')

    short_sleep()

    textbox = find_element_with_retry(driver,By.ID,"setup-page-team-name")
    if textbox == None:
        if find_element_with_retry(driver,By.CSS_SELECTOR,'span.c-alert__message[data-qa-alert-message="true"]') != None:
            time.sleep(1800)
            return
    textbox.send_keys(Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE)
    textbox.send_keys(random.choice(string.ascii_uppercase) + datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))

    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="setup-page-team-name-submit"]')

    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="setup-page-profile-submit"]')

    short_sleep()

    click_element_with_retry(driver,By.CLASS_NAME,"c-link--button.p-setup_page__content_secondary_link.no_wrap.margin_left_0.margin_top_50")

    short_sleep()

    click_element_with_retry(driver,By.CLASS_NAME,"c-button.c-button--danger.c-button--medium")

    short_sleep()


    textbox = find_element_with_retry(driver,By.ID,"setup-channel-name-input")
    textbox.click()
    textbox.send_keys("ztry")

    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="step-channels-footer-next"]')


    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="setup_flow_tada_coachmark_cta"]')

    short_sleep()

    click_element_with_retry(driver,By.CLASS_NAME,"nudge_left_1.p-channel_sidebar__section_heading_more_label")

    short_sleep()

    click_element_with_retry(driver,By.XPATH,"//div[text()='Slack Connect']")

    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="sk_close_modal_button"]')

    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="slack_connect_landing_page__channel_cta"]')

    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="trial_entry_point_modal_start_trial_button"]')

    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="modal_speed_bump_continue"]')

    short_sleep()

    textbox = find_element_with_retry(driver,By.ID,"channel-name")
    textbox.send_keys("try_claude")

    #此处必须long sleep，使用short sleep有概率报错。
    long_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="create-channel-next-button"]')

    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="create-channel-next-button"]')

    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="invite_to_workspace_skip_button"]')

    short_sleep()

    workspace_url = driver.current_url

    driver.get("https://slackbot.anthropic.com/slack/install")

    #必须long_sleep
    long_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="oauth_submit_button"]')

    short_sleep()

    driver.get(workspace_url)

    long_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="texty_mention_button"]')

    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'span[data-qa="member_name__app"]')

    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="texty_send_button"]')

    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="at_mention_invite_warning__invite_button"]')

    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="texty_mention_button"]')

    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'span[data-qa="member_name__app"]')

    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="texty_send_button"]')

    short_sleep()

    click_element_with_retry(driver,By.XPATH,"//span[text()='Agree']")

    short_sleep()

    click_element_with_retry(driver,By.CSS_SELECTOR,'button[data-qa="dialog_go"]')

    long_sleep()

    return

def main():

    options = webdriver.EdgeOptions()
    options.add_argument("-inprivate")

    driver = webdriver.Edge(options=options)

    #打开登录页面，url为要打开的地址
    driver.get("https://slack.com/intl/zh-cn/get-started")

    #元素定位登录按钮

    textbox = find_element_with_retry(driver,By.ID,"creator_signup_email")
    #点击登录
    textbox.click()
    textbox.send_keys(username)

    #等待
    short_sleep()

    click_element_with_retry(driver,By.ID,"submit_btn")

    short_sleep()
    '''
    commit_code = get_latest_mail().replace("-", "")

    commit_textbox = find_element_with_retry(driver,By.CSS_SELECTOR,'.split_input_item input[aria-label="6 个中的第 1 位数字"]')
    commit_textbox.send_keys(commit_code)
    '''
    short_sleep()

    create_new_area(driver)

    while(1):
        driver.get("https://slack.com/intl/zh-cn/get-started")
        create_new_area(driver)
    
if __name__ == '__main__':
    main()
