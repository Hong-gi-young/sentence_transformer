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
from dateutil.relativedelta import relativedelta
from utube import *
from shorts import shorts_crawling
warnings.filterwarnings('ignore')

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--disable-gpu')  
driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)


# 인기 급상승 동영상 url
user_url = "https://www.youtube.com/feed/explore"
driver.get(user_url) 
time.sleep(4)

#인기 급상승 동영상 가져오기
soup = soup_find(driver)
informations = soup.find({'id':'contents','class':'style-scope ytd-item-section-renderer'}).findAll('ytd-video-renderer',class_='style-scope ytd-expanded-shelf-contents-renderer')

for inform in informations:
    #url
    url = inform.find('a',{'id':'channel-thumbnail','class':'yt-simple-endpoint inline-block style-scope ytd-thumbnail'})['href']
    url = "https://www.youtube.com"+url
    urls.append(url)
    
    #유튜버이름
    name = inform.find('a',class_='yt-simple-endpoint style-scope yt-formatted-string').get_text().strip()
    print('name',name)
    #영상제목
    title = inform.find('yt-formatted-string',class_='style-scope ytd-video-renderer').get_text().strip()
    print('title',title)
    #조회수
    counts = inform.find('span',class_='style-scope ytd-video-meta-block')[0].get_text().strip()
    print('counts',counts)
    #날짜
    original_times = inform.find('span',class_='style-scope ytd-video-meta-block')[1].get_text().strip()
    
    #날짜 변환
    if "년" in original_times:
        year = original_times.split('년')[0]
        year = str(now - relativedelta(years=int(year))).split(" ")[0]
        print("년 단위:",year)
        times.append(year)
        
    elif "개월" in original_times:
        month = original_times.split('개월')[0]
        month = str(now - relativedelta(months=int(month))).split(" ")[0]       
        print("개월 단위:",month)
        times.append(month)
        
    elif "주" in original_times:
        week = original_times.split('주')[0]
        week = str(now - relativedelta(weeks=int(week))).split(" ")[0]       
        print("주 단위:",week)
        times.append(week)
        
    elif "일" in original_times:
        day = original_times.split('일')[0]
        day = str(now - relativedelta(days=int(day))).split(" ")[0]    
        print("일 단위:",day) 
        times.append(day)
    else:
        second = str(now).split(" ")[0]     
        print("초:",second)
        times.append(second)
   
