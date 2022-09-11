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
from dateutil.relativedelta import relativedelta
warnings.filterwarnings('ignore')


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)

#target of crawling
data_list = []
driver.get("https://www.youtube.com/watch?v=QndOyQtTHUQ")
time.sleep(10)
first_page = driver.execute_script("return document.documentElement.scrollHeight")
# 스크롤 내리기
def scroll_down(driver):
    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    # while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(3)
    new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    
        # if new_page_height == last_page_height:
        #     break

# 시간체크
now = datetime.now()

#스크롤 다운
scroll_down(driver)
time.sleep(1)
driver.execute_script("window.scrollTo(0,500)")
time.sleep(3)
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
print('조회수',view_counts)

# 영상 좋아요 수
good_counts = soup.find('yt-formatted-string',class_='style-scope ytd-toggle-button-renderer style-text').get_text()
print('좋아요',good_counts)


# 댓글 크롤링
comments = soup.find('ytd-app').find('div',class_='style-scope ytd-app').find('ytd-page-manager',class_='style-scope ytd-app').find('div',id='columns').findAll('ytd-comment-thread-renderer')
# print(comments)
for comment in comments:
    
    #댓글 text
    print('\n')
    text = comment.find('div',{"id":'comment-content','class':'style-scope ytd-comment-renderer'}).get_text().replace('자세히 보기','').replace('간략히','').replace('\n','') .strip()
    print('text',text)
    
    #작성자
    author = comment.find('a',id='author-text').get_text().strip()
    print('작성자',author)
    
    # 공감
    agree_counts = comment.find('span',class_='style-scope ytd-comment-action-buttons-renderer').get_text().strip()
    print('공감',agree_counts)
    
    #시간 크롤링
    original_times = comment.find('a',class_='yt-simple-endpoint style-scope yt-formatted-string').get_text().replace('(수정됨)','').strip()
    print('시간',original_times)
    
    #날짜로 변환
    if "년" in original_times:
        year = original_times.split('년')[0]
        times = str(now - relativedelta(years=int(year))).split(" ")[0]
        print("년 단위:",times)
        
    elif "개월" in original_times:
        month = original_times.split('개월')[0]
        times = str(now - relativedelta(months=int(month))).split(" ")[0]       
        print("개월 단위:",times)
        
    elif "주" in original_times:
        month = original_times.split('주')[0]
        times = str(now - relativedelta(weeks=int(month))).split(" ")[0]       
        print("주 단위:",times)
        
    elif "일" in original_times:
        month = original_times.split('일')[0]
        times = str(now - relativedelta(days=int(month))).split(" ")[0]    
        print("일 단위:",times) 
    else:
        times = str(now).split(" ")[0]     
        print("초:",times)