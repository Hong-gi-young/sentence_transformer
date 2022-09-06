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
warnings.filterwarnings('ignore')


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)

#target of crawling
data_list = []
driver.get("https://www.youtube.com/watch?v=QndOyQtTHUQ")
time.sleep(4)

# 스크롤 내리기
def scroll_down(driver):
    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    # while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(3)
    new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        # if new_page_height == last_page_height:
        #     break
        
# 동영상제목
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')
title = soup.find("script",class_='style-scope ytd-player-microformat-renderer').get_text() #뽑을수 있는 데이터는 다뽑자
# title = eval(title)
# print(type(title))
# print(title['name'])

# 구독자 수
counts = soup.find('yt-formatted-string',id='owner-sub-count').get_text()
print(counts)
# 채널명
name = soup.find('div',class_='style-scope ytd-channel-name').find('a',class_='yt-simple-endpoint style-scope yt-formatted-string').get_text()
print(name)

# 조회수
view_counts = soup.find('span',class_='view-count style-scope ytd-video-view-count-renderer').get_text().split(' ')[1]
print(view_counts)

# 영상 좋아요 수
good_counts = soup.find('yt-formatted-string',class_='style-scope ytd-toggle-button-renderer style-text').get_text()
print(good_counts)

#스크롤 다운
scroll_down(driver)

# 댓글 크롤링
comments = soup.findall('ytd-comment-thread-renderer')
for comment in comments:
    
## id
## 공감