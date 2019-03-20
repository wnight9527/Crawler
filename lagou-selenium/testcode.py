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
from datetime import datetime, date, timedelta

publishTimeTemp = '12:00 发布'
publishTime = (date.today() + timedelta(days=-re.findall("\d+", publishTimeTemp)[0])).strftime("%Y-%m-%d") if publishTimeTemp.find('天前发布') == True else  publishTimeTemp if publishTimeTemp.find('发布') == False else (date.today()).strftime("%Y-%m-%d")

print(publishTime)
# if '3天前发布'.find('天前发布') == True :
#     yesterday = date.today() + timedelta(days=-1)  # 昨天日期
#     yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
#     print(yesterday)
# ss = '23tian'
# s = re.findall("\d+",ss)[0]
# print(s)
# SalaryTWO = re.match(r'(.*?)k-(.*?)k', Salarymini, re.M | re.I)
# print(SalaryTWO.group(1))

# for number in range(0, 31):
#
#     if  number <= 12:
#         print(number)
#     else:
#         break
#
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
