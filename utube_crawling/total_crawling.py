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
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--disable-software-rasterizer')
driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)

# url 
"""
1. https://www.youtube.com/c/DickHunter/featured
-> https://www.youtube.com/c/DickHunter/videos 변경

2. 정렬기준 클릭 후 3 Types 선택

3. URL 수집 

4. df = one_crawling() 실행

5. df concat 실행
"""