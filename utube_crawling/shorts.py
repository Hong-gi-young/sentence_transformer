# 크롤링 라이브러리 Import
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import random
import warnings
import itertools
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dateutil.relativedelta import relativedelta
from utube import *


warnings.filterwarnings('ignore')
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--disable-gpu')  
driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)

# 스크롤 내리기
def scroll_downh(driver):
    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(1)
    
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(3)
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        print('스크롤 내리기')
        if new_page_height == last_page_height:
            break 
        last_page_height = new_page_height
        
def shorts_scroll(driver):
    # locator(즉, 스크롤할 위치) 지정
    reply_body  = driver.find_element(By.XPATH, "//div[@id='contents']") 
    # 참고. selector로도 지정가능 ->  reply_body  = driver.find_element(By.CSS_SELECTOR, "#contents") 

    last_height = driver.execute_script("return arguments[0].scrollHeight", reply_body) 

    while True:    
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].scrollHeight;', reply_body)
        time.sleep(1.5)
    
        new_height = driver.execute_script("return  arguments[0].scrollHeight" , reply_body) 
        
        print('last_height: ', last_height, 'new_height: ', new_height)

        if new_height == last_height:
            break

        last_height = new_height 
        time.sleep(1.5)

# url 
# def url_transform():
# 동영상 코너로 변환
user_url = "https://www.youtube.com/shorts/Rm1IorQTDbk"
driver.get(user_url) 
time.sleep(5)

#페이지소스
soup = soup_find(driver)

#동영상제목
title = soup.find('h2',class_='title style-scope ytd-reel-player-header-renderer').get_text().strip()
print('title',title)
#채널명
name = soup.find('div',{'id':'channel-container','class':'style-scope ytd-reel-player-header-renderer'}).find('a',class_='yt-simple-endpoint style-scope yt-formatted-string').get_text()
print('name',name)

#영상좋아요
good_count = soup.find('div',{'id':'actions','class':'style-scope ytd-reel-player-overlay-renderer'}).find('yt-formatted-string',class_='style-scope ytd-toggle-button-renderer style-text').get_text()
print('good_count',good_count)

##댓글 가져오기
#댓글 클릭
driver.find_element_by_xpath('//*[@id="comments-button"]').click()
time.sleep(1)

#스크롤
shorts_scroll(driver)

#페이지소스
soup2 = soup_find(driver)

#댓글

#작성자
#공감
#시간크롤링
#날짜로 변환


"""
1. short 구별하는 문자 출력
2. short로 이동후 크롤링.

* short url 따로 담아서 shrot만 or 동영상만 할수 있도록 조건문 처리.


"""