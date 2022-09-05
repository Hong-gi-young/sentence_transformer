# 크롤링 라이브러리 Import
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import gensim
import time
from gensim import corpora
import pyLDAvis.gensim_models
from eunjeon import Mecab
import random
import warnings
import itertools
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
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
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(3)
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_page_height == last_page_height:
            break
        
# 동영상제목
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')
title = soup.find("script",class_='style-scope ytd-player-microformat-renderer').get_text()
title = eval(title)
print(type(title))
print(title['name'])










# 채널명
# 조회수
# 영상 좋아요 수
# 댓글 크롤링
# 작성자 크롤링
# 공감 비공감 크롤링