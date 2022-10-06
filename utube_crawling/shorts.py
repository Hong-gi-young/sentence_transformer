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
from datetime import datetime,timedelta
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

def shorts_crawling():
    authors,texts,agree_counts,times = [],[],[],[]
    user_url = "https://www.youtube.com/shorts/Rm1IorQTDbk"
    driver.get(user_url) 
    time.sleep(5)

    # 시간체크
    now = datetime.now()

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

    # 설명 클릭
    driver.find_element_by_xpath('//*[@id="menu"]/ytd-menu-renderer').click()
    time.sleep(2)
        
    driver.find_element_by_xpath('//*[@id="items"]/ytd-menu-service-item-renderer').click()
    time.sleep(1)
    
    # 조회수
    soup_temp = soup_find(driver)
    view_counts = soup_temp.findAll('yt-formatted-string',class_='factoid-value style-scope ytd-factoid-renderer')[1].get_text().strip()
    print('조회수:',view_counts)
    
    #닫기 버튼
    driver.find_element_by_xpath('//*[@id="visibility-button"]').click()
    time.sleep(2)
    
    ##댓글 가져오기
    #댓글 클릭
    driver.find_element_by_xpath('//*[@id="comments-button"]').click()
    time.sleep(1)

    #스크롤
    shorts_scroll(driver)

    #페이지소스
    soup2 = soup_find(driver)

    #댓글
    replies = soup2.find('div',{'id':'contents','class':'style-scope ytd-item-section-renderer'}).findAll('ytd-comment-thread-renderer',class_='style-scope ytd-item-section-renderer')
    for reply in replies:
        text = reply.find('yt-formatted-string',id='content-text').get_text().strip()
        texts.append(text)
        print('\n')
        print('text:',text)

        #고정댓글 작성자
        try: 
            author = reply.find('yt-formatted-string',{'id':'text','class':'style-scope ytd-channel-name'}).get_text().strip()
            authors.append(author)
            print('작성자:',author)
            
        #일반 작성자
        except:
            author = reply.find('a',{'id':'author-text','class':'yt-simple-endpoint style-scope ytd-comment-renderer'}).find('span',class_=' style-scope ytd-comment-renderer').get_text().strip()
            authors.append(author)
            print('작성자:',author)
                
        #공감
        agree_count = reply.find('span',{'id':'vote-count-middle','class':'style-scope ytd-comment-action-buttons-renderer'}).get_text().strip()
        agree_counts.append(agree_count)
        print('공감수:',agree_count)
        
        #시간크롤링
        original_times = reply.find('a',class_='yt-simple-endpoint style-scope yt-formatted-string').get_text().strip()
        
        #날짜로 변환
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
    print('댓글총 갯수',len(replies))
    information = {'유튜버':name,
                    "영상제목":title,
                    '조회수':view_counts,
                    '좋아요':good_count,
                    '작성자':authors,
                    '댓글':texts,
                    '공감':agree_counts,
                    '시간':times}
    df = pd.DataFrame(information)

    return df
# if __name__ == '__main__':
#     shorts_crawling()
