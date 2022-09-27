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
from dateutil.relativedelta import relativedelta
from utube import *

warnings.filterwarnings('ignore')
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--disable-gpu')  
driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)

# url 
# def url_transform():
# 동영상 코너로 변환
user_url = "https://www.youtube.com/c/DickHunter/featured"
url_splited = user_url.split('/')
if url_splited[-1] =='featured':
    user_url = user_url.replace('featured', 'videos') 
    print('user_url:',user_url)
    
driver.get(user_url) 
time.sleep(5)
# 영상 선택 기준
# step 1) 업로드한 영상 + 정렬기준

def uploaded_videos(sorting_value='인기 동영상'):
    
    #정렬기준 선택
    driver.find_element_by_xpath('//*[@id="sort-menu"]/yt-sort-filter-sub-menu-renderer/yt-dropdown-menu').click()
    time.sleep(1)

    # 추가된 날짜(오래된순)
    if sorting_value == '추가된 날짜(오래된순)':
        driver.find_element_by_xpath('//*[@id="menu"]/a[2]').click()
        time.sleep(1)

    # 추가된 날짜(최신순)
    elif sorting_value == '추가된 날짜(최신순)':
        driver.find_element_by_xpath('//*[@id="menu"]/a[3]').click()
        time.sleep(1)

    else:
        pass #인기동영상(defalt value)

def videos_select_options(selected_options='업로드한 동영상'):
    
    # 업로드된 동영상 칸 클릭
    driver.find_element_by_xpath('//*[@id="label"]/paper-ripple').click()
    
    
    # 전체동영상인 경우
    if selected_options == '전체 동영상':       
        #전체동영상클릭
        driver.find_element_by_xpath('//*[@id="menu"]/a[1]/tp-yt-paper-item').click()
        time.sleep(1)
        
    elif selected_options == '이전 실시간 스트림':
        #이전 실시간 스트림 클릭
        driver.find_element_by_xpath('//*[@id="menu"]/a[3]/tp-yt-paper-item').click()
        time.sleep(1)
    
    else:
        uploaded_videos()
        time.sleep(1)

# 스크롤 다운

def scroll_down():
    while True:
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(3)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_heigh

#3. URL 수집 
# def urls_crawling(counts=np.inf):
counts=2 #np.inf # 특정 갯수 만큼 가져오기
urls = []
soup = soup_find(driver)
information_all = soup.find('div',{'id':'contents','class':'style-scope ytd-item-section-renderer'}).find_all('ytd-grid-video-renderer',class_='style-scope ytd-grid-renderer')
for idx,inform in enumerate(information_all):
    
    url = inform.find('a',class_='yt-simple-endpoint inline-block style-scope ytd-thumbnail')['href']
    url = "https://www.youtube.com"+url
    
    #short 걸러내기
    # if 'shorts' in url:
    #     continue
    idx = idx+1 
    urls.append(url)
    print(url)
    print('idx',idx)
    if counts == idx: 
        break
    
total_df = pd.DataFrame()
for url in urls:
    df = one_crawling(url)
    # concat 실행
    total_df = pd.concat([total_df,df])
    print('pass')
driver.close()
    
    
    
    
    
    
# def main():
# total = pd.DataFrame()
# for url in urls[::]:
#     # 정보 긁어오기
#     df = one_crawling(url)
    
#     # concat 실행
#     total_df = pd.concat([total,df])
    

