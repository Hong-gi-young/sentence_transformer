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
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--disable-gpu')  
driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)


def popular_video_crawling(user_url="https://www.youtube.com/feed/explore"):
    driver.get(user_url) 
    time.sleep(4)

    #인기 급상승 동영상 가져오기
    urls,names,titles,video_lens,view_counts,times=[],[],[],[],[],[]
    soup = soup_find(driver)
    now = datetime.now()
    informations = soup.findAll('ytd-video-renderer',class_='style-scope ytd-expanded-shelf-contents-renderer')
    # print(informations)

    for inform in informations:
        #url
        url = inform.find('a',{'id':'thumbnail','class':'yt-simple-endpoint inline-block style-scope ytd-thumbnail'})['href']
        url = "https://www.youtube.com"+url
        urls.append(url)
        
        #유튜버이름
        name = inform.find('a',class_='yt-simple-endpoint style-scope yt-formatted-string').get_text().strip()
        print('name',name)
        names.append(name)
        
        #영상제목
        title = inform.find('yt-formatted-string',class_='style-scope ytd-video-renderer').get_text().strip()
        print('title',title)
        titles.append(title)
        
        #영상길이
        video_len = inform.find('span',{'id':'text','class':'style-scope ytd-thumbnail-overlay-time-status-renderer'}).get_text().strip()
        print('영상길이',video_len)
        video_lens.append(video_len)
        
        #조회수
        view_count = inform.find_all('span',class_='inline-metadata-item style-scope ytd-video-meta-block')[0].get_text().split(' ')[1].strip()
        
        if "억회" in view_count:
            view_count = view_count.replace('.','').replace('억회','00000000').strip() 
        
        elif "만회" in view_count:
            view_count = view_count.replace('.','').replace('만회','0000').strip() 
        
        elif "천회" in view_count:
            view_count = view_count.replace('.','').replace('천회','000').strip() 
        else:
            view_count = view_count.replace('회',"").strip()
        print('view_count',view_count)
        view_counts.append(int(view_count))
        
        #날짜
        original_times = inform.find_all('span',class_='inline-metadata-item style-scope ytd-video-meta-block')[1].get_text().strip()
        
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
        print('\n')
        
    information = {'유튜버':names,
                    "영상제목":titles,
                    '조회수':view_counts,
                    "영상길이":video_lens,
                    '업로드한 시간':times}

    #저장하기
    df = pd.DataFrame(information)
    df.to_excel(f'{str(now).split(" ")[0]}_인급동.xlsx')
    driver.close()

if __name__=='__main__':
    popular_video_crawling()