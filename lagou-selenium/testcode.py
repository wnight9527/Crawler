# -*- coding: utf-8 -*-
# author:wnight 白夜
import requests
import re
import time
from selenium import webdriver
from lxml import etree
import csv
from pyquery import PyQuery as pq
import time
import random
import json
import requests
import pymongo
# from config import *
from bs4 import BeautifulSoup
import random
import time

for number in range(0, 31):

    if  number <= 12:
        print(number)
    else:
        break
# path = "C:\Program Files\Tencent\QQBrowser\chromedriver.exe"
# chrome_options = webdriver.ChromeOptions()
#
# b = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
# b.get('https://www.lagou.com/jobs/list_{}?city={}&cl=false&fromSearch=true&labelWords=&suginput='.format('java','上海'))
#
# soup = BeautifulSoup(b.page_source, 'lxml')
# Administratives = soup.select('div > div.choose-detail > div > div:nth-child(2) > a')
#
# for Administrative in Administratives:
#     data =  Administrative.get_text()
#     if data == '不限':
#         pass
#     else:
#         print(data)